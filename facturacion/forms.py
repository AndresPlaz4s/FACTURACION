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
                "rows":4,
                "placeholder": "descripcion breve del producto",
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
        fields =["nombre","email","n_documento"]
        widgets = {
                "nombre": forms.TextInput( attrs={
                    "placeholder": "ingrese el nombre",
                }),
                "email": forms.EmailInput(attrs={
                    "placeholder":"ingrese su email",
                }),
                "n_documento":forms.NumberInput(attrs={
                    "step": 1,
                    "min": 0,
                })
    }
    

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, label='Contraseña')
    password2 = forms.CharField(widget=forms.PasswordInput, required=False, label='Confirmar contraseña')
    class Meta:
        model = Usuario
        fields = ["nombre", "email", "rol"]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "placeholder": "ingrese el nombre",
            }),
            "email": forms.EmailInput(attrs={
                    "placeholder":"ingrese su email",
                }),
            
            "rol": forms.Select()
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

