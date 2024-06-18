from django import forms
from .models import Producto, Categoria

class ProductoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all()

    class Meta:
        model = Producto
        fields = ['nombre', 'marca', 'modelo', 'descripcion', 'precio', 'codigo', 'imagen', 'categoria', 'observaciones', 'especificaciones']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'})  # Agrega la clase form-control para el estilo (si lo deseas)
        }
        
        
# forms.py

from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'direccion', 'telefono', 'email', 'documentocliente']
        
