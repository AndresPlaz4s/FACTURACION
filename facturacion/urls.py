from django.urls import path
from . import views

app_name = 'facturacion'

urlpatterns = [
    path('home/', views.home, name='home'),

    path('ventas/', views.ventas, name='ventas'),

    path('inventario/', views.inventario, name='inventario'),
    path('inventario/crear_producto/', views.crear_producto, name="crear_producto"),
    path('inventario/<int:pk>/editar_producto/', views.editar_producto, name="editar_producto"),
    path('inventario/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),

    path('facturas/', views.facturas, name='facturas'),

    path('usuarios/', views.usuarios, name='usuarios'),
    
     #clientes
    path('cliente/', views.cliente, name='cliente'),
    path('cliente/crear_cliente', views.crear_cliente, name='crear_cliente'),
]