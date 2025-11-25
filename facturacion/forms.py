from django import forms
from django.forms import inlineformset_factory
from .models import Producto, Cliente, Usuario   


"formulario para registrar productos"

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "precio", "stock", "tipo", "descripcion", "f_vencimiento" ]
        widgets = {
            "nombre": forms.TextInput( attrs={
                "placeholder": "nombre del Producto",
            }),
            "precio": forms.NumberInput(attrs={
                "step": 10,
                "min": 0,
            }),
            "stock": forms.NumberInput(attrs={
                "step": 1,
                "min": 0,
            }),
            "descripcion": forms.Textarea(attrs={
            "rows": 4,
            "placeholder": "descripcion breve del producto",
            "class": "descripcion-textarea"
            }),
            "f_vencimiento": forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            })
        }
    def clean_precio(self):
        precio = self.cleaned_data.get("precio")
        if precio is not None and precio <= 0:
            raise forms.ValidationError("El precio tiene que ser mayor a 0")
        return precio

"formulario para registrar cliente"

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "email", "n_documento"]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "placeholder": "Nombre del cliente",
                'class': 'form-control',
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Ingrese su correo electrónico",
                'class': 'form-control',
            }),
            "n_documento": forms.NumberInput(attrs={
                "step": 1,
                "min": 0,
                "placeholder": "Documento del cliente",
                'class': 'form-control',
            }),
        }

def clean_n_documento(self):
    n_documento = self.cleaned_data.get("n_documento")

    if n_documento is None or n_documento == "":
        raise forms.ValidationError("Debe ingresar un número de documento")

    if not str(n_documento).isdigit():
        raise forms.ValidationError("El documento debe contener solo números")

    n_documento = int(n_documento)

    if n_documento <= 0:
        raise forms.ValidationError("El número de documento debe ser mayor a 0")

    return n_documento



class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, label='Contraseña')
    password2 = forms.CharField(widget=forms.PasswordInput, required=False, label='Confirmar contraseña')
    class Meta:
        model = Usuario
        fields = ["nombre", "email", "rol"]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "placeholder": "ingrese el nombre",
                'class': 'form-control',
            }),
            "email": forms.EmailInput(attrs={
                    "placeholder":"ingrese su email",
                    'class': 'form-control',
                }),
            
            "rol": forms.Select(),
            'class': 'form-control',
        }

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('password2')
        
        if not getattr(self, 'instance', None) or not self.instance.pk:
            if not p1:
                raise forms.ValidationError('La contraseña es obligatoria para crear un usuario.')
            if not p2:
                raise forms.ValidationError('Debe confirmar la contraseña.')
        
        if p1 or p2:
            if p1 != p2:
                raise forms.ValidationError('Las contraseñas no coinciden.')
        return cleaned

