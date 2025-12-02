from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils.dateparse import parse_date
from weasyprint import HTML, CSS
from datetime import date, timedelta
from django.db.models import Sum, F, DecimalField, QuerySet
import json

from .models import Producto, Cliente, Usuario, Venta, Factura, DetalleVenta
from .forms import ProductoForm, ClienteForm, UsuarioForm, UserEditForm
from decimal import Decimal


@login_required
def home(request):
    return render(request, 'facturacion/home.html')



@login_required
def ventas(request):
    clientes = Cliente.objects.all()
    productos = Producto.objects.all()

    if request.method == "POST":
        try:
            data = json.loads(request.POST.get("data") or "{}")

            cliente_id = data.get("cliente")
            items = data.get("productos", [])
            forma_pago = data.get("forma_pago", "EFECTIVO")

            if not cliente_id:
                messages.error(request, "Debe seleccionar un cliente.")
                return redirect("facturacion:ventas")

            if len(items) == 0:
                messages.error(request, "Debe agregar productos.")
                return redirect("facturacion:ventas")

            cliente = get_object_or_404(Cliente, id=cliente_id)

            # validar stock
            for item in items:
                prod = get_object_or_404(Producto, id=item["id"])
                if int(item.get("cantidad", 0)) > prod.stock:
                    messages.error(request, f"Stock insuficiente para {prod.nombre}")
                    return redirect("facturacion:ventas")

            # crear venta
            venta = Venta.objects.create(
                cliente=cliente,
                usuario=request.user,
                forma_pago=forma_pago
            )

            # crear detalles y descontar stock
            for item in items:
                prod = get_object_or_404(Producto, id=item["id"])
                cant = int(item.get("cantidad", 0))
                p_unit = Decimal(str(prod.precio))
                total = (p_unit * cant).quantize(Decimal("0.01"))

                DetalleVenta.objects.create(
                    venta=venta,
                    producto=prod,
                    cantidad=cant,
                    p_unitario=p_unit,
                    total=total
                )

                prod.stock -= cant
                prod.save()

            # crear factura asociada a la venta
            Factura.objects.create(
                venta=venta,
                forma_pago=forma_pago
            )

            messages.success(request, "Venta registrada correctamente.")
            # Redirige a la vista de pdf (según tu URLconf)
            return redirect("facturacion:factura_pdf", pk=venta.id)

        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect("facturacion:ventas")

    return render(request, "facturacion/ventas.html", {
        "clientes": clientes,
        "productos": productos,
    })
    
    
    
@login_required
def editar_venta(request, pk):
    venta = get_object_or_404(Venta, id=pk)
    clientes = Cliente.objects.all()
    detalles = DetalleVenta.objects.filter(venta=venta)
    productos = Producto.objects.all()

    if request.method == "POST":
        data = json.loads(request.POST.get("data"))
        cliente = Cliente.objects.get(id=data["cliente"])
        venta.cliente = cliente
        venta.save()

        # devolver stock anterior
        for d in detalles:
            d.producto.stock += d.cantidad
            d.producto.save()

        detalles.delete()

        # crear nuevos detalles
        for item in data["items"]:
            p = Producto.objects.get(id=item["id"])
            cant = int(item["cantidad"])
            total = cant * p.precio

            DetalleVenta.objects.create(
                venta=venta,
                producto=p,
                cantidad=cant,
                p_unitario=p.precio,
                total=total
            )

            p.stock -= cant
            p.save()

        return redirect("facturacion:factura_pdf", pk=venta.id)

    return render(request, "facturacion/editar_venta.html", {
        "venta": venta,
        "clientes": clientes,
        "productos": productos,
        "detalles": detalles
    })


@login_required
def inventario(request):

    if request.GET.get("ok"):
        producto = Producto.objects.all().order_by("nombre")
        return render(request, 'facturacion/inventario.html', {"producto": producto})

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/partials/inventario.html')

    producto = Producto.objects.all().order_by("nombre")
    bajo_stock = producto.filter(stock__lte=10)

    if bajo_stock.exists():
        return redirect("facturacion:alerta_bajo_stock")

    return render(request, 'facturacion/inventario.html', {"producto": producto})


@login_required
def alerta_bajo_stock(request):
    bajo_stock = Producto.objects.filter(stock__lte=10).order_by("nombre")
    return render(request, "facturacion/alerta_bajo_stock.html", {
        "bajo_stock": bajo_stock
    })


@login_required
def alert_vencimiento(request):
    hoy = date.today()

    bajo_stock = Producto.objects.filter(stock__lte=10)
    p_vencidos = Producto.objects.filter(f_vencimiento__lt=hoy)
    pronto_vencer = Producto.objects.filter(f_vencimiento__lte=hoy + timedelta(days=31))

    return render(request, "facturacion/alerta_bajo_stock.html", {
        "bajo_stock": bajo_stock,
        "p_vencidos": p_vencidos,
        "pronto_vencer": pronto_vencer,
    })


@login_required
def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("facturacion:inventario")
    else:
        form = ProductoForm()

    return render(request, 'facturacion/crear_producto.html', {"form": form})


@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("facturacion:inventario")
    else:
        form = ProductoForm(instance=producto)

    return render(request, "facturacion/editar_producto.html", {
        "form": form,
        "producto": producto
    })


@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        producto.delete()
        return redirect("facturacion:inventario")

    return render(request, "facturacion/eliminar_producto.html", {
        "producto": producto
    })


@login_required
def cliente(request):
    cliente = Cliente.objects.all().order_by("nombre")
    return render(request, 'facturacion/cliente.html', {"cliente": cliente})


@login_required
def crear_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("facturacion:cliente")
    else:
        form = ClienteForm()

    return render(request, 'facturacion/crear_cliente.html', {"form": form})


@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect("facturacion:cliente")
    else:
        form = ClienteForm(instance=cliente)

    return render(request, "facturacion/editar_cliente.html", {
        "form": form,
        "cliente": cliente
    })


@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == "POST":
        cliente.delete()
        return redirect("facturacion:cliente")

    return render(request, "facturacion/eliminar_cliente.html", {
        "cliente": cliente
    })


@login_required
def usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'facturacion/usuarios.html', {'usuarios': usuarios})


@login_required
def crear_usuario(request):
    if request.method == "POST":
        user_form = UserEditForm(request.POST)
        perfil_form = UsuarioForm(request.POST)

        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save()
            perfil = perfil_form.save(commit=False)
            perfil.user = user
            perfil.save()

            messages.success(request, "Usuario creado correctamente")
            return redirect('facturacion:usuarios')

    else:
        user_form = UserEditForm()
        perfil_form = UsuarioForm()

    return render(request, "facturacion/crear_usuario.html", {
        "user_form": user_form,
        "perfil_form": perfil_form
    })


@login_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    user = usuario.user

    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=user)
        perfil_form = UsuarioForm(request.POST, instance=usuario)

        if user_form.is_valid() and perfil_form.is_valid():

            # guardar usuario
            user = user_form.save()

            # si escribió contraseña
            nueva_pass = user_form.cleaned_data.get("password1")
            if nueva_pass:
                user.set_password(nueva_pass)
                user.save()

            # guardar perfil
            perfil_form.save()

            return redirect("facturacion:usuarios")

    else:
        user_form = UserEditForm(instance=user)
        perfil_form = UsuarioForm(instance=usuario)

    return render(request, "facturacion/editar_usuario.html", {
        "user_form": user_form,
        "perfil_form": perfil_form,
        "usuario": usuario,
    })


@login_required
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    user = usuario.user

    if request.method == "POST":
        usuario.delete()
        user.delete()
        return redirect("facturacion:usuarios")

    return render(request, "facturacion/eliminar_usuario.html", {
        "usuario": usuario,
        "user": user
    })



def generar_factura_pdf(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    detalles = venta.detalles.all()

    total_general = sum(d.total for d in detalles)

    html_string = render_to_string('facturacion/transacciones/factura_pdf.html', {
        'venta': venta,
        'detalles': detalles,
        'total_general': total_general,
        'request': request,
    })

    pdf = HTML(string=html_string).write_pdf()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=factura_{pk}.pdf'
    response.write(pdf)
    return response



@login_required
def facturas(request):
    fecha = request.GET.get("fecha")

    qs: QuerySet = Factura.objects.select_related(
        "venta",
        "venta__cliente"
    ).prefetch_related(
        "venta__detalles"
    )

    if fecha:
        fecha = parse_date(fecha)
        qs = qs.filter(fecha__date=fecha)
    qs = qs.annotate(
        total_factura=Sum(
            F("venta__detalles__cantidad") * F("venta__detalles__p_unitario"),
            output_field=DecimalField()
        )
    ).order_by("-fecha")

    return render(request, "facturacion/facturas.html", {
        "ventas": qs,
        "fecha": fecha
    })
