from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Sum
from django.utils.dateparse import parse_date

class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField(max_length=200, blank=True, null=True)
    n_documento = models.CharField(max_length=10, blank=True, null=True)
    
    class Meta:
        db_table = 'cliente'
        
    
    def __str__(self):
        return f"{self.nombre} ({self.n_documento})"

class Usuario(models.Model):

    ROL_CHOICES = [
        ("administrador", "Administrador"),
        ("vendedor", "Vendedor"),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil'
    )
    
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default="vendedor")

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return f"{self.user.username} - {self.rol}"

class Administrador(models.Model):
    nombre = models.CharField(max_length=50 )
    email = models.EmailField(max_length=200, blank=True, null=True)
    contrasena = models.CharField(max_length=128, help_text='Almacenar hashed/backed value, no texto plano')
    n_documento = models.CharField(max_length=10, blank=True, null=True)
    rol = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        db_table = 'administrador'
    
    def __str__(self):
        return f"{self.nombre} ({self.rol or 'admin'})"

class Proveedor(models.Model):
    nit = models.CharField(max_length=9, unique=True)
    n_empresa = models.CharField(max_length=50)
    contacto = models.CharField(max_length=10, blank=True, null=True)
    
    class Meta:
        db_table = 'proveedor'
    
    def __str__(self):
        return f"{self.n_empresa} ({self.nit})"

class Producto(models.Model):
    TIPO_PRODUCTO = [
        ("CAJA", "Caja"),
        ("BL", "Bl"),
        ("UNIDAD", "Unidad"),
    ]

    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=10, choices=TIPO_PRODUCTO)
    f_entrada = models.DateField(auto_now_add=True)
    f_vencimiento = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'producto'

    def __str__(self):
        return f"{self.nombre}"

class ProveedorProducto(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    c_productos = models.IntegerField()
    
    class Meta:
        db_table = 'proveedor_producto'
        unique_together = (('proveedor', 'producto'),)
    
    def __str__(self):
        return f"{self.proveedor.n_empresa} -> {self.producto.nombre}: {self.c_productos}"

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    fecha = models.DateTimeField(default=timezone.now)
    forma_pago = models.CharField(max_length=20, choices=[("EFECTIVO","Efectivo"),("TRANSFERENCIA","Transferencia")], default="EFECTIVO")

    class Meta:
        db_table = 'venta'

    def __str__(self):
        return f"Venta #{self.pk}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    p_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "detalle_venta"

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"


class Factura(models.Model):

    FORMAS_PAGO = [
        ('EFECTIVO', 'Efectivo'),
        ('TRANSFERENCIA', 'Transferencia'),
    ]

    ESTADOS = [
        ('PAGADA', 'Pagada'),
        ('ANULADA', 'Anulada'),
    ]

    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="facturas")
    codigo = models.CharField(max_length=20, unique=True, blank=True)
    forma_pago = models.CharField(max_length=20, choices=FORMAS_PAGO)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PAGADA')
    fecha = models.DateTimeField(default=timezone.now)
    

    class Meta:
        db_table = 'factura'

    def __str__(self):
        return f"Factura {self.codigo} - {self.estado}"

    def save(self, *args, **kwargs):
        if not self.codigo:
            ultimo = Factura.objects.order_by('-id').first()
            numero = (ultimo.id + 1) if ultimo else 1
            self.codigo = f"FAC-{numero}"

        super().save(*args, **kwargs)

