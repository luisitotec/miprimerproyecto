"""
URL configuration for InformaticaWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from tienda.views import agregar_producto
from tienda.views import lista_productos
from tienda.views import crear_venta, detalle_venta
from tienda.views import ingresar_series
from tienda.views import lista_existencias
from tienda.views import obtener_detalle_producto
from tienda.views import generar_catalogo_pdf
from tienda.views import crear_categoria
from tienda.views import cargar_categorias
from tienda.views import generar_catalogo_pdf_por_categoria
from tienda.views import venta_masiva
from tienda.views import AutocompleteProductos
from tienda.views import detalle_producto
from tienda.views import cliente_view
from tienda.views import lista_clientes
from tienda.views import procesamiento_ventamasiva
from tienda.views import reporte_ventas, crear_factura
from tienda.views import inventario_productos
from tienda.views import ingresar_proveedor
from tienda.views import trazabilidad_series
from tienda.views import inicio
from tienda.views import registrar_usuario
from tienda.views import login
from tienda.views import stock_view
from tienda.views import stock_grupal
from tienda.views import logout_view
from tienda.views import detalles_venta_modal

from tienda.views import emitir_reporte_ventas




urlpatterns = [
    path("admin/", admin.site.urls),
    path('', login, name='login'),
    path('inicio/', inicio, name='inicio'),  # URL raíz que carga la página de inicio
    path('agregar_producto/', agregar_producto, name='agregar_producto'),
    path('lista_productos/', lista_productos, name='lista_productos'),
    path('crear_venta/', crear_venta, name='crear_venta'),
    path('venta/<int:venta_id>/', detalle_venta, name='detalle_venta'),
    path('venta/<int:venta_id>/factura/', crear_factura, name='crear_factura'),
    path('inventario_productos/', inventario_productos, name='inventario_productos'),
    path('ingresar_proveedor/', ingresar_proveedor, name='ingresar_proveedor'),
    path('trazabilidad-series/', trazabilidad_series, name='trazabilidad_series'),
    path('stock/', stock_view, name='stock'),
    path('stock-grupal/', stock_grupal, name='stock_grupal'),
    path('detalles-venta-modal/<int:venta_id>/', detalles_venta_modal, name='detalles_venta_modal'),
    path('emitir-reporte-ventas/', emitir_reporte_ventas, name='emitir_reporte_ventas'),
    
    
    path('ingresar_series/', ingresar_series, name='ingresar_series'),
    path('lista_existencias/', lista_existencias, name='lista_existencias'),
    path('obtener_detalle_producto/<int:producto_id>/', obtener_detalle_producto, name='obtener_detalle_producto'),
    path('generar_catalogo_pdf/', generar_catalogo_pdf, name='generar_catalogo_pdf'),
    path('crear_categoria/', crear_categoria, name='crear_categoria'),
    path('cargar_categorias/',cargar_categorias, name='cargar_categorias'),
    path('generar_catalogo_pdf_por_categoria/<int:categoria_id>/',generar_catalogo_pdf_por_categoria, name='generar_catalogo_pdf_por_categoria'),
    path('venta-masiva/', venta_masiva, name='venta_masiva'),
    path('autocomplete/productos/', AutocompleteProductos.as_view(), name='autocomplete_productos'),
    path('detalle_producto/<str:codigo>/', detalle_producto, name='detalle_producto'),
    path('cliente/', cliente_view, name='cliente_form'),
    path('lista_clientes/', lista_clientes, name='lista_clientes'),
    path('procesamiento_ventamasiva/', procesamiento_ventamasiva, name='procesamiento_ventamasiva'),
    path('reporte_ventas/',reporte_ventas, name='reporte_ventas'),
    path('registrar/', registrar_usuario, name='registrar_usuario'),
    
    path('logout/', logout_view, name='logout'),


]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)