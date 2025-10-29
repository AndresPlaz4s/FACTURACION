from django.urls import path
from . import views

app_name = 'facturacion'

urlpatterns = [
    path('', views.home, name='navbar'),
    path('ventas/', views.ventas, name='ventas'),
    path('inventario/', views.inventario, name='inventario'),
    path('facturas/', views.facturas, name='facturas'),
    path('usuarios/', views.usuarios, name='usuarios'),
]
