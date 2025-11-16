from django import forms
from django.forms import inlineformset_factory
from .models import Producto, Cliente


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
    