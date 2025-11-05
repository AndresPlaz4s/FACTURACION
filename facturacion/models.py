from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    Contraseña  = models.CharField(max_length= 20, blank= False, null= False)
    Tipo_Usuario = models.CharField(max_length= 20, blank= False, null= False)
    def __str__(self):
        return f"{self.nombre} <{self.correo}>"
    
