from django.shortcuts import render
from django.http import HttpResponse 
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, 'facturacion/home.html')

@login_required
def ventas(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/partials/ventas.html')
    return render(request, 'facturacion/ventas.html')

@login_required
def inventario(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/partials/inventario.html')
    return render(request, 'facturacion/inventario.html')

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