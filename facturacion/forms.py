from django import forms
from django.forms import inlineformset_factory
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "precio", "stock", "descripcion", "f_vencimiento" ]
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
