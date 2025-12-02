from django import forms
from django.forms import inlineformset_factory
from .models import Producto, Cliente, Usuario, User
from django.contrib.auth.forms import UserCreationForm

"formulario para registrar productos"

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "precio", "stock", "tipo", "descripcion", "f_vencimiento" ]
        widgets = {
            "nombre": forms.TextInput(attrs={
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
            "f_vencimiento": forms.DateInput(
                format='%Y-%m-%d',         
                attrs={
                    'type': 'date',         
                    'class': 'form-control'
                }
            )
        }

    #bloque importante
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['f_vencimiento'].input_formats = ['%Y-%m-%d']
        
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





class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        
        
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["rol"]
        widgets = {
            "rol": forms.Select(attrs={"class": "form-control"}),
        }
        
class UserEditForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput,
        required=False
    )
    password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = User
        fields = ["username", "email"]
        labels = {
            "username": "Nombre de usuario",
            "email": "Correo electrónico"
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 or p2:
            if p1 != p2:
                raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data