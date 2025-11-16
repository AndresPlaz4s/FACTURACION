from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse 
from django.contrib.auth.decorators import login_required

from .models import Producto, Cliente

from .forms import ProductoForm , ClienteForm

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

@login_required
def usuarios(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/partials/usuarios.html')
    return render(request, 'facturacion/usuarios.html')

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
