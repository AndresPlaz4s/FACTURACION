from django.db import models

""""class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    Contraseña  = models.CharField(max_length= 20, blank= False, null= False)
    Tipo_Usuario = models.CharField(max_length= 20, blank= False, null= False)
    def __str__(self):
        return f"{self.nombre} <{self.correo}>"""""
    
class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField(max_length=200, blank=True, null=True)
    n_documento = models.CharField(max_length=10, unique=False, blank=True, null=True)

    class Meta:
        db_table = 'cliente'

    def __str__(self):
        return f"{self.nombre} ({self.n_documento})"

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField(max_length=200, blank=True, null=True)
    n_documento = models.CharField(max_length=10, unique=False, blank=True, null=True)
    rol = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return f"{self.nombre} - {self.rol or 'sin rol'}"

class Administrador(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField(max_length=200, blank=True, null=True)
    contrasena = models.CharField(max_length=128, help_text='Almacenar hashed/backed value, no texto plano')
    n_documento = models.CharField(max_length=10, unique=False, blank=True, null=True)
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
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)
    f_entrada = models.DateField(blank=True, null=True)
    f_vencimiento = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'producto'

    def __str__(self):
        return f"{self.nombre} - {self.stock} unidades"

class ProveedorProducto(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, db_column='id_proveedor')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto')
    c_productos = models.IntegerField()

    class Meta:
        db_table = 'proveedor_producto'
        unique_together = (('proveedor', 'producto'),)

    def __str__(self):
        return f"{self.proveedor.n_empresa} -> {self.producto.nombre}: {self.c_productos}"

class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, db_column='id_producto')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, db_column='id_cliente')
    cantidad = models.IntegerField()
    p_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'venta'

    def __str__(self):
        return f"Venta #{self.pk or '-'}: {self.producto.nombre} x{self.cantidad} = {self.total}"

    def save(self, *args, **kwargs):
        try:
            calc_total = (self.p_unitario or 0) * (self.cantidad or 0)
        except Exception:
            calc_total = self.total or 0
        if not self.total or float(self.total) != float(calc_total):
            self.total = calc_total
        super().save(*args, **kwargs)
