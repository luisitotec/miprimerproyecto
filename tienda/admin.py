from django.contrib import admin
from .models import Producto
from .models import Cliente
from .models import Existencia
from .models import Venta
from .models import DetalleVenta
from .models import Categoria
from .models import Proveedor
from .models import Sucursal
from .models import Usuario



# Register your models here.


admin.site.register(Producto)


admin.site.register(Cliente)

admin.site.register(Existencia)

admin.site.register(Venta)

admin.site.register(Proveedor)

admin.site.register(Sucursal)

admin.site.register(Usuario)



class DetalleVentaAdmin(admin.ModelAdmin):
 list_display = ('venta', 'producto', 'cantidad', 'precio_unitario', 'descuento', 'impuesto', 'formatted_series_vendidas')

admin.site.register(DetalleVenta, DetalleVentaAdmin)

admin.site.register(Categoria)









