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
    path('cliente/crear_cliente/', views.crear_cliente, name='crear_cliente'),
    path('cliente/<int:pk>/editar_cliente/', views.editar_cliente, name='editar_cliente'),
    path('cliente/<int:pk>/eliminar_cliente/', views.eliminar_cliente, name='eliminar_cliente'),


    
    path('usuario/', views.usuario_login, name='usuario_login'),
    path('usuario/crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('usuario/<int:pk>/editar_usuario/', views.editar_usuario, name='editar_usuario'),
    path('usuario/<int:pk>/eliminar_usuario/', views.eliminar_usuario, name='eliminar_usuario'),
    path('ventas/', views.ventas, name='ventas'),
]



