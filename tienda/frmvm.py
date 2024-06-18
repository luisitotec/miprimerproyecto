from django import forms
from .models import Venta

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = [
            'tipo_operacion', 'departamento', 'municipio', 'registro', 'giro', 
            'metodo_pago', 'condicionesPago'
        ]
        widgets = {
            'tipo_operacion': forms.Select(attrs={'id': 'id_tipoOperacion', 'name': 'tipoOperacion'}),
            'departamento': forms.TextInput(attrs={'id': 'id_departamento', 'name': 'departamento'}),
            'municipio': forms.TextInput(attrs={'id': 'id_municipio', 'name': 'municipio'}),
            'registro': forms.TextInput(attrs={'id': 'id_registro', 'name': 'registro'}),
            'giro': forms.TextInput(attrs={'id': 'id_giro', 'name': 'giro'}),
            'metodo_pago': forms.Select(attrs={'id': 'id_metodoPago', 'name': 'metodoPago'}),
            'condicionesPago': forms.Select(attrs={'id': 'id_condicionesPago', 'name': 'condicionesPago'}),
        }
