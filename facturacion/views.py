from django.shortcuts import render
from django.http import HttpResponse 
from django.contrib.auth.decorators import login_required


@login_required
def ventas(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/ventas.html')
    return render(request, 'facturacion/partials/navbar.html')

@login_required
def inventario(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/inventario.html')
    return render(request, 'facturacion/partials/navbar.html')

@login_required
def facturas(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/facturas.html')
    return render(request, 'facturacion/partials/navbar.html')

@login_required
def usuarios(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/usuarios.html')
    return render(request, 'facturacion/partials/navbar.html')
