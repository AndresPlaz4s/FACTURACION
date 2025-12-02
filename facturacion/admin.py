from django.contrib import admin
from facturacion.models import Usuario, Cliente, Producto, Venta, DetalleVenta, Factura


# Register your models here.

admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(Factura)