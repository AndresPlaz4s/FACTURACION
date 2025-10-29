from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'facturacion/partials/navbar.html')

def ventas(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/ventas.html')
    return render(request, 'facturacion/partials/navbar.html')

def inventario(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/inventario.html')
    return render(request, 'facturacion/partials/navbar.html')

def facturas(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/facturas.html')
    return render(request, 'facturacion/partials/navbar.html')

def usuarios(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/usuarios.html')
    return render(request, 'facturacion/partials/navbar.html')
