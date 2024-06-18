from django.db import models

# Create your models here.
from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    documentocliente = models.CharField(max_length=100)


    def __str__(self):
        return self.nombre


from django.db import models
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    # Elimina la descripción si no la necesitas o si está causando problemas
    
    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    codigo = models.CharField(max_length=50, unique=True)
    stock = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)  # Ajusta según sea necesario
    observaciones = models.TextField(blank=True, null=True)
    especificaciones = models.TextField(blank=True, null=True)
    otra_categoria = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if self.otra_categoria:
            categoria, created = Categoria.objects.get_or_create(nombre=self.otra_categoria)
            self.categoria = categoria

        super().save(*args, **kwargs)  # Llamar primero al método save() de la superclase

        # Actualizar el stock del producto después de guardar
        self.update_stock()

    def update_stock(self):
        self.stock = Existencia.objects.filter(producto=self, estado='Disponible').count()
        super().save(update_fields=['stock'])  # Guardar solo el campo 'stock' para evitar ciclos infinitos

    def __str__(self):
        return self.nombre





   
   
##################### MODELO VENTA ############################################

from django.db import models

class Venta(models.Model):
    TIPO_OPERACION_CHOICES = [
        ('FAC_CONSUMIDOR_FINAL', 'Factura Consumidor Final'),
        ('CREDITO_FISCAL', 'Crédito Fiscal'),
    ]
    
    METODO_PAGO_CHOICES = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta'),
        ('DEPOSITO', 'Deposito Bancario'),
        ('GIRO', 'Remesa'),
        ('BITCOIN', 'Bitcoin')
    ]
    
    
    tipo_operacion = models.CharField(max_length=50, choices=TIPO_OPERACION_CHOICES, default='FAC_CONSUMIDOR_FINAL')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    documentocliente = models.CharField(max_length=100)
    condicionesPago = models.CharField(max_length=100)
    direccioncliente = models.CharField(max_length=100)
    vendedor = models.CharField(max_length=100, default="Sin nombre")
    
    metodo_pago = models.CharField(max_length=50, choices=METODO_PAGO_CHOICES, default='EFECTIVO')
       
    
    
    estado = models.CharField(max_length=50, choices=[
        ('En proceso', 'En proceso'),
        ('Completado', 'Completado')
    ])
    
    
    
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Campos adicionales para Crédito Fiscal
    municipio = models.CharField(max_length=100, blank=True, null=True)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    registro = models.CharField(max_length=100, blank=True, null=True)
    nit = models.CharField(max_length=100, blank=True, null=True)
    giro = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Venta {self.id} - {self.cliente}"

    def total_venta(self):
        detalles = DetalleVenta.objects.filter(venta=self)
        total = sum(detalle.subtotal() for detalle in detalles)
        return total





from datetime import datetime


    
class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, blank=True, null=True)
    encargado = models.CharField(max_length=100, blank=True, null=True)
    bodega = models.CharField(max_length=100)  # Campo para indicar la bodega asociada a la sucursal

    def __str__(self):
        return self.nombre 
    

class Existencia(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    numero_serie = models.CharField(max_length=100, unique=True)
    estado = models.CharField(max_length=50, choices=[('Disponible', 'Disponible'), ('Vendido', 'Vendido')])
    ubicacion = models.CharField(max_length=100)
    id_venta = models.IntegerField(blank=True, null=True)
    nombreProveedor = models.CharField(max_length=100)
    ordenCompra = models.CharField(max_length=100)
    fechaIngreso = models.DateField()  # Se elimina auto_now_add=True
    nfacturaCompra = models.CharField(max_length=100)
    observaciones = models.CharField(max_length=500)
    lote = models.CharField(max_length=100, blank=True, null=True)  # Añadir campo lote
    caux1 = models.CharField(max_length=100)
    caux2 = models.CharField(max_length=100)
    caux3 = models.CharField(max_length=100)
    operador = models.CharField(max_length=100, default='Admin')  
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, default=1)  # Definición de la clave foránea
    cantidad = models.IntegerField(default=1)  # Cantidad de unidades de producto en esta existencia

    
    
    
    def __str__(self):
        return self.numero_serie







from django.utils.html import format_html
    

    
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    numeros_serie = models.TextField(blank=True, null=True)  # Campo existente para almacenar números de serie
    series_vendidas = models.TextField(blank=True)
    
    existencia = models.ForeignKey('Existencia', on_delete=models.SET_NULL, null=True, blank=True, related_name='detalleventa_set')
    
    def __str__(self):
        return f"Detalle de Venta {self.venta.id} - {self.producto} x {self.cantidad}"

    def subtotal(self):
        return (self.cantidad * self.precio_unitario) - self.descuento + self.impuesto

    def formatted_series_vendidas(self):
        if self.series_vendidas:
            series_list = self.series_vendidas.split(',')
            return format_html('<br>'.join(series_list))
        return ''

    formatted_series_vendidas.short_description = 'Series Vendidas'
    


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, blank=True, null=True)
    sitio_web = models.URLField(max_length=200, blank=True, null=True)
    rubro = models.CharField(max_length=100, blank=True, null=True)
    representante = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre
    

    
    
    
# models.py en la app 'tienda'

from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100, default="Sin nombre")
    email = models.EmailField(unique=True)
    departamento = models.CharField(max_length=100)
    password = models.CharField(max_length=128, default="")  # Valor predeterminado para el campo password
    # Otros campos según tus necesidades

    def __str__(self):
        return self.nombre
