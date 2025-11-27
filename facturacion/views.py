from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

from .models import Producto, Cliente, Usuario, Venta

from .forms import ProductoForm, ClienteForm, UsuarioForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
import json

from django.template.loader import render_to_string
from weasyprint import HTML

@login_required
def home(request):
    return render(request, 'facturacion/home.html')

@login_required
def ventas(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/partials/ventas.html')
    return render(request, 'facturacion/ventas.html')

#productos (CRUD)

@login_required
def inventario(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/partials/inventario.html')
    producto = Producto.objects.all().order_by("nombre")
    return render(request, 'facturacion/inventario.html', {"producto": producto})


@login_required
def crear_producto(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/partials/inventario.html')
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

    return render(request, "facturacion/editar_producto.html", 
                    {"form": form, 
                    "producto": producto
                        })


@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        producto.delete()
        return redirect("facturacion:inventario")
    return render(
        request,
        "facturacion/eliminar_producto.html",
        {
            "producto": producto
        }
    )



@login_required
def facturas(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/partials/facturas.html')
    return render(request, 'facturacion/facturas.html')
#USUARIOS BRAYAN
@login_required
def usuarios(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/partials/usuarios.html')
    usuarios = Usuario.objects.all().order_by('nombre')
    return render(request, 'facturacion/usuarios.html', {'usuarios': usuarios})


def usuario_login(request):
    
    if request.user.is_authenticated:
        return redirect('facturacion:usuarios')

    next_url = request.GET.get('next') or request.POST.get('next')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url or 'facturacion:usuarios')
        else:
            error = 'Credenciales inválidas. Verifica usuario y contraseña.'
    return render(request, 'registration/login.html', {'error': error, 'next': next_url})



@login_required
def crear_usuario(request):
   
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/partials/usuarios.html')
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            
            usuario_obj = form.save(commit=False)
            
            username = usuario_obj.email if usuario_obj.email else usuario_obj.nombre
            password = form.cleaned_data.get('password')

            if User.objects.filter(username=username).exists():
                form.add_error('email', 'Ya existe un usuario con ese email/usuario en el sistema.')
            else:
                
                user = User.objects.create_user(username=username, email=usuario_obj.email or '', password=password)
                
                usuario_obj.user = user
                usuario_obj.save()
                
                login(request, user)
                messages.success(request, 'Usuario creado y sesión iniciada correctamente.')
                
                return redirect('facturacion:usuarios')
    else:
        form = UsuarioForm()  
    return render(request, 'facturacion/crear_usuario.html', {"form": form})

@login_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            
            user = None
            if usuario.user:
                user = usuario.user
            else:
                if usuario.email:
                    try:
                        user = User.objects.filter(email=usuario.email).first()
                        if user:
                            usuario.user = user
                            usuario.save()
                    except User.DoesNotExist:
                        user = None

            nuevo_password = form.cleaned_data.get('password')

            # guardar cambios en Usuario local
            usuario = form.save()

            # si se proporcionó nueva contraseña y existe User, actualizarla
            if nuevo_password and user:
                user.set_password(nuevo_password)
                user.save()

            return redirect("facturacion:usuarios")

    else:
        form = UsuarioForm(instance=usuario)

    return render(
        request,
        "facturacion/editar_usuario.html",
        {
            "form": form,
            "usuario": usuario
        }
    )



@login_required
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == "POST":
        usuario.delete()
        return redirect("facturacion:usuarios")
    return render(
        request,
        "facturacion/eliminar_usuario.html",
        {"usuario": usuario}
    )

#cliente. smith

@login_required
def cliente (request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/partials/usuarios.html')
    cliente = Cliente.objects.all().order_by("nombre")
    return render(request, 'facturacion/cliente.html', {"cliente": cliente})

@login_required
def crear_cliente(request):
    # Si es AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/partials/cliente.html')
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

    return render(
        request,
        "facturacion/editar_cliente.html",
        {
            "form": form,
            "cliente": cliente
        }
    )



@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        cliente.delete()
        return redirect("facturacion:cliente")
    return render(
        request,
        "facturacion/eliminar_cliente.html",
        {"cliente": cliente}
    )
    
@login_required
def ventas(request):
    clientes = Cliente.objects.all()
    productos = Producto.objects.all()
    
    if request.method == "POST":
        try:
            data = json.loads(request.POST.get("data"))
            cliente_id = data.get("cliente")
            productos_json = data.get("productos", [])
            
            if not cliente_id:
                messages.error(request, "Debe seleccionar un cliente.")
                return redirect("facturacion:ventas")
            
            if len(productos_json) == 0:
                messages.error(request, "Debe agregar productos a la venta.")
                return redirect("facturacion:ventas")
            
            cliente = Cliente.objects.get(id=cliente_id)
            
            # Validar stock antes de crear las ventas
            for item in productos_json:
                prod = Producto.objects.get(id=item["id"])
                cantidad = int(item["cantidad"])
                if cantidad > prod.stock:
                    messages.error(request, f"Stock insuficiente para {prod.nombre}")
                    return redirect("facturacion:ventas")
            
            # Crear ventas individuales y guardar el ID de la primera
            primera_venta_id = None
            
            for item in productos_json:
                prod = Producto.objects.get(id=item["id"])
                cantidad = int(item["cantidad"])
                total = prod.precio * cantidad
                
                venta = Venta.objects.create(
                    producto=prod,
                    cliente=cliente,
                    cantidad=cantidad,
                    p_unitario=prod.precio,
                    total=total
                )
                
                # Guardar el ID de la primera venta para el PDF
                if primera_venta_id is None:
                    primera_venta_id = venta.id
                
                # Descontar stock
                prod.stock -= cantidad
                prod.save()
            
            messages.success(request, "Venta registrada correctamente.")
            # Redirigir al PDF de la primera venta
            return redirect("facturacion:factura_pdf", pk=primera_venta_id)
            
        except Exception as e:
            messages.error(request, f"Error en la venta: {str(e)}")
            return redirect("facturacion:ventas")
    
    return render(request, "facturacion/ventas.html", {
        "clientes": clientes,
        "productos": productos,
    })
# ==================== GENERACIÓN DE PDF ====================
def generar_factura_pdf(request, pk):
    """
    Genera una factura en PDF para una venta específica.
    """
    venta = get_object_or_404(Venta, pk=pk)
    
    # Obtener todas las ventas del mismo cliente (asumiendo que son de la misma transacción)
    # Si tu modelo Venta tiene un campo fecha, usa: fecha__date=venta.fecha.date()
    # Como no lo tiene, obtenemos solo las ventas relacionadas por cliente
    ventas_relacionadas = Venta.objects.filter(
        cliente=venta.cliente,
        id__gte=pk  # Ventas desde este ID en adelante (misma transacción)
    ).select_related('producto')
    
    # Calcular total
    total_general = sum(v.total for v in ventas_relacionadas)
    
    # Renderizar el template HTML
    html_string = render_to_string('facturacion/transacciones/factura_pdf.html', {
        'venta': venta,
        'detalles': ventas_relacionadas,
        'total_general': total_general,
        'request': request,
    })
    
    # Generar PDF con WeasyPrint
    html = HTML(string=html_string)
    result = html.write_pdf()
    
    # Crear respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=factura_venta_{venta.id}.pdf'
    response.write(result)
    
    return response