from django import forms
from .models import Venta, DetalleVenta, Existencia

class VentaForm(forms.ModelForm):

    class Meta:
        model = Venta
        fields = [
            'tipo_operacion', 'cliente', 'documentocliente', 'condicionesPago', 'direccioncliente', 'metodo_pago',
            'municipio', 'departamento', 'registro', 'giro'
        ]
        widgets = {
              
        }
    
    
    
    
    
    
    
class DetalleVentaForm(forms.ModelForm):
    numeros_serie = forms.CharField(max_length=500, required=False, label='Números de Serie (separados por comas)')

    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad', 'precio_unitario', 'descuento', 'impuesto']



# En forms.py

from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'rubro', 'representante', 'direccion', 'telefono', 'email']




# User
from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'departamento']







from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario', max_length=100)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
