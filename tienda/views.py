from django.shortcuts import render, redirect
from django.http import JsonResponse
from tienda.ProductoForm import ProductoForm
from django.http import JsonResponse
from django.forms.models import inlineformset_factory
from datetime import date


from django.shortcuts import render

def inicio(request):
    usuario = request.session.get('usuario')
    return render(request, 'inicio.html', {'usuario': usuario})







def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': '¡Producto ingresado correctamente!'})
        else:
            return JsonResponse({'success': False, 'message': 'Error al ingresar el producto'})
    else:
        form = ProductoForm()
    
    return render(request, 'agregar_producto.html', {'form': form})




from django.shortcuts import render
from .models import Producto, Categoria

def lista_productos(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()  # Obtener todas las categorías disponibles
    context = {
        'productos': productos,
        'categorias': categorias,  # Pasar las categorías al contexto del template
    }
    return render(request, 'lista_productos.html', context)

# Vista para crear la venta

from django.shortcuts import render
from django.http import JsonResponse
from django.forms import inlineformset_factory
from datetime import date
from django.contrib.auth.decorators import login_required  # Importa el decorador de autenticación
from django.contrib.auth.models import User 
import json
from .models import Venta, DetalleVenta, Cliente, Existencia, Producto
from .forms import VentaForm, DetalleVentaForm


def crear_venta(request):
    usuario = request.session.get('usuario')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            venta_data = data.get('venta', {})
            detalles_data = data.get('detalles', [])
            total = data.get('total', 0)

            # Obtener o crear el cliente
            cliente_nombre = venta_data.get('cliente')
            cliente, created = Cliente.objects.get_or_create(nombre=cliente_nombre)
            if created:
                print(f"Cliente '{cliente_nombre}' creado.")
            else:
                print(f"Cliente '{cliente_nombre}' obtenido.")

            # Obtener tipo de operación seleccionado
            tipo_operacion = venta_data.get('tipo_operacion')

            # Crear la instancia de la venta con el cliente y tipo de operación
            venta = Venta(
                cliente=cliente,
                fecha=venta_data.get('fecha'),
                documentocliente=venta_data.get('documentocliente'),
                condicionesPago=venta_data.get('condicionesPago'),
                direccioncliente=venta_data.get('direccioncliente'),
                metodo_pago=venta_data.get('metodo_pago'),
                municipio=venta_data.get('municipio'),
                departamento=venta_data.get('departamento'),
                registro=venta_data.get('registro'),
                giro=venta_data.get('giro'),
                estado=venta_data.get('estado'),
                total=total,
                tipo_operacion=tipo_operacion,  # Asignar el tipo de operación seleccionado
                vendedor=usuario  # Asignar el usuario al campo vendedor
            )
            venta.save()

            # Guardar los detalles de la venta
            for detalle_data in detalles_data:
                try:
                    # Obtener el producto por su código
                    codigo_producto = detalle_data['codigo']
                    producto = Producto.objects.get(codigo=codigo_producto)

                    # Verificar si hay suficiente stock
                    cantidad_vendida = 0
                    for serie in detalle_data['series_vendidas']:
                        cantidad_vendida += 1  # Contar cada serie vendida

                    if cantidad_vendida > producto.stock:
                        return JsonResponse({'error': f"No hay suficiente stock para el producto {producto.nombre}"}, status=400)

                    # Crear un detalle por cada serie vendida
                    for serie in detalle_data['series_vendidas']:
                        detalle = DetalleVenta(
                            venta=venta,
                            producto=producto,
                            cantidad=1,  # Cada serie vendida cuenta como una unidad
                            precio_unitario=detalle_data['precio_unitario'],
                            descuento=detalle_data['descuento'],
                            impuesto=detalle_data['impuesto'],
                            series_vendidas=serie  # Aquí se guarda una serie individual
                        )
                        detalle.save()

                        # Actualizar el estado de las existencias a "Vendido"
                        existencia = Existencia.objects.get(numero_serie=serie)
                        existencia.id_venta = venta.id  # Asigna el id de la venta a id_venta en Existencia
                        existencia.venta = venta
                        existencia.estado = 'Vendido'
                        existencia.save()

                    # Restar el stock del producto vendido
                    producto.stock -= cantidad_vendida
                    producto.save()

                    # Actualizar el stock del producto (si es necesario, dependiendo de la lógica en tu modelo Producto)
                    producto.update_stock()

                    # Log each detail saved
                    print(f"Detalle guardado para producto {producto.nombre}")

                except Producto.DoesNotExist:
                    return JsonResponse({'error': f"Producto '{detalle_data['producto']}' no encontrado."}, status=400)
                except Existencia.DoesNotExist:
                    return JsonResponse({'error': f"Serie no encontrada en el inventario."}, status=400)
                except Exception as e:
                    return JsonResponse({'error': f"Error al guardar el detalle: {str(e)}"}, status=500)

            # Log successful sale
            print("Venta creada con éxito:", venta)

            return JsonResponse({'venta_id': venta.id})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON no válido'}, status=400)
        except Exception as e:
            # Log unexpected errors
            print("Error inesperado:", str(e))
            return JsonResponse({'error': 'Error inesperado', 'details': str(e)}, status=500)

    else:
        # Para GET request, obtener solo los productos con existencias disponibles
        productos_disponibles = Producto.objects.filter(
            existencia__estado='Disponible'
        ).distinct()

        for producto in productos_disponibles:
            producto.existencias = Existencia.objects.filter(producto=producto, estado='Disponible')

        VentaDetalleFormSet = inlineformset_factory(Venta, DetalleVenta, form=DetalleVentaForm, extra=0, can_delete=True)

        venta_form = VentaForm()
        formset = VentaDetalleFormSet()
        fecha_actual = date.today()

        tipo_operacion_choices = Venta.TIPO_OPERACION_CHOICES

        return render(request, 'crear_venta.html', {
            'usuario': usuario,
            'productos': productos_disponibles,
            'venta_form': venta_form,
            'formset': formset,
            'fecha_actual': fecha_actual,
            'tipo_operacion_choices': tipo_operacion_choices,
        })















        
def actualizar_series_descargar(series):
# Función para actualizar el área de la interfaz de usuario que muestra las series a descargar
# Implementar según la estructura de tu plantilla
    pass


# Es lo que sale despues de la venta
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Min
from .models import Venta, DetalleVenta

def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)
    cliente = venta.cliente  # Asegúrate de obtener correctamente el cliente asociado a la venta

    return render(request, 'detalle_venta.html', {
        'venta': venta,
        'detalles': detalles,
        'cliente': cliente,
    })
    
    
    
    
    
    
# Ingreso de series:

from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Existencia, Proveedor  
from .models import Producto, Existencia, Sucursal  
from django.http import HttpResponse
from datetime import datetime 

def ingresar_series(request):
    usuario = request.session.get('usuario')
    productos = Producto.objects.all()
    proveedores = Proveedor.objects.all()  # Obtén todos los proveedores
    sucursales = Sucursal.objects.all()  # Obtén todas las sucursales

    if request.method == 'POST':
        producto_id = request.POST['producto_id']
        producto = get_object_or_404(Producto, id=producto_id)
        lote = request.POST['lote']
        ubicacion_id = request.POST['sucursal']  # Cambiar para obtener el ID de la sucursal
        ubicacion = get_object_or_404(Sucursal, id=ubicacion_id)  # Obtener el objeto de Sucursal
        fecha_ingreso_str = request.POST['fecha_ingreso']
        fecha_ingreso = datetime.strptime(fecha_ingreso_str, '%Y-%m-%d').date()
        numeros_serie = request.POST['numeros_serie'].split()
        proveedor_id = request.POST['proveedor']  # Obtener el ID del proveedor seleccionado
        proveedor = get_object_or_404(Proveedor, id=proveedor_id)  # Obtener el objeto de Proveedor
        orden_compra = request.POST['orden_compra']
        nfactura_compra = request.POST['nfactura_compra']
        observaciones = request.POST['observaciones']

        for numero_serie in numeros_serie:
            Existencia.objects.create(
                producto=producto,
                numero_serie=numero_serie,
                ubicacion=ubicacion,
                estado='Disponible',
                nombreProveedor=proveedor.nombre,
                ordenCompra=orden_compra,
                fechaIngreso=fecha_ingreso,
                nfacturaCompra=nfactura_compra,
                observaciones=observaciones,
                lote=lote,  # Añadir lote aqu
                operador = usuario
            )

        # Actualiza el stock del producto después de ingresar las series
        producto.stock = Existencia.objects.filter(producto=producto).count()
        producto.save()

        return redirect('ingresar_series')  # Redirige a la misma página para ingresar más series

        
    # Envía productos, proveedores y sucursales al contexto del template
    return render(request, 'ingresar_series.html', {'productos': productos, 'proveedores': proveedores, 'sucursales': sucursales, 'usuario': usuario})

    










#Lista de existencias
from django.shortcuts import render
from .models import Existencia

def lista_existencias(request):
    existencias = Existencia.objects.all()
    return render(request, 'lista_existencias.html', {'existencias': existencias})

# Obtener el detalle de los productos

from django.http import JsonResponse
from .models import Producto

#def obtener_detalle_producto(request, producto_id):
   # try:  
     #   producto = Producto.objects.get(id=producto_id)
      #  data = {
       #     'nombre': producto.nombre,
         #   'descripcion': producto.descripcion,
          #  'precio': producto.precio,
            # Otros detalles del producto que desees devolver
        #}
        #return JsonResponse(data)
    #except Producto.DoesNotExist:
     #   return JsonResponse({'error': 'Producto no encontrado'}, status=404)



# Vista auxiliar para manejar la solicitud AJAX

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Producto

def obtener_detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    series = producto.existencia_set.values_list('numero_serie', flat=True)
    data = {
        'nombre': producto.nombre,
        'descripcion': producto.descripcion,
        'precio': producto.precio,
        'codigo': producto.codigo,
        'series': list(series)
    }
    return JsonResponse(data)




from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from .models import Producto
from reportlab.lib.styles import getSampleStyleSheet



# Generar catalogo PDF de todos los productos

def generar_catalogo_pdf(request):
    # Obtener todos los productos
    productos = Producto.objects.all()
    
    

    # Crear un objeto BytesIO para almacenar el PDF en memoria
    buffer = BytesIO()

    # Crear un documento PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Crear una lista para almacenar los elementos del catálogo
    content = []

    # Agregar título al catálogo
    content.append(Paragraph("Catálogo de Productos", styles['Title']))

    for producto in productos:
        # Agregar la categoría
        content.append(Paragraph(f"<b>{producto.categoria}</b>", styles['Heading2']))

        # Agregar el nombre del producto
        content.append(Paragraph(producto.nombre, styles['Heading3']))

        # Agregar la imagen
        imagen = Image(producto.imagen.path, width=185, height=185)
        content.append(imagen)

        # Agregar el precio
        content.append(Paragraph(f"Precio: {producto.precio}", styles['Normal']))

        # Agregar las especificaciones
        content.append(Paragraph(f"Especificaciones: {producto.especificaciones}", styles['Normal']))

        # Agregar un espacio entre productos
        content.append(Spacer(1, 12))

    # Agregar el contenido al documento
    doc.build(content)

    # Obtener el valor del buffer
    pdf = buffer.getvalue()
    buffer.close()

    # Crear una respuesta HTTP con el contenido del PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="catalogo_productos.pdf"'
    response.write(pdf)

    return response



from django.shortcuts import render, redirect
from .models import Categoria

def crear_categoria(request):
    if request.method == 'POST':
        nombre_categoria = request.POST.get('nombre_categoria')
        if nombre_categoria:
            try:
                nueva_categoria = Categoria.objects.create(nombre=nombre_categoria)
                # Puedes agregar lógica adicional aquí si es necesario
                return JsonResponse({'success': True})  # Devolver una respuesta JSON indicando éxito
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})  # Manejar errores de creación de la categoría
        else:
            return JsonResponse({'success': False, 'message': 'Nombre de categoría no proporcionado'})
    else:
        return JsonResponse({'success': False, 'message': 'Método de solicitud no válido'})
        
# Cargar categorias

from django.http import JsonResponse
from .models import Categoria

def cargar_categorias(request):
    categorias = Categoria.objects.all().values('id', 'nombre')
    return JsonResponse(list(categorias), safe=False)



# Catalogo por categoria

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from .models import Producto

def generar_catalogo_pdf_por_categoria(request, categoria_id):
    try:
        # Obtener la categoría por su ID
        categoria = get_object_or_404(Categoria, id=categoria_id)

        # Obtener todos los productos de la categoría
        productos = Producto.objects.filter(categoria=categoria)

        if not productos.exists():
            raise Exception("No hay productos para esta categoría.")

        # Crear un objeto BytesIO para almacenar el PDF en memoria
        buffer = BytesIO()

        # Crear un documento PDF
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        # Crear una lista para almacenar los elementos del catálogo
        content = []

        # Agregar título al catálogo
        content.append(Paragraph(f"Catálogo de Productos - {categoria.nombre}", styles['Title']))

        for producto in productos:
            # Agregar el nombre del producto
            content.append(Paragraph(producto.nombre, styles['Heading3']))

            # Agregar la descripción
            content.append(Paragraph(producto.descripcion, styles['Normal']))

            # Agregar la imagen si existe
            if producto.imagen:
                try:
                    imagen = Image(producto.imagen.path, width=185, height=185)
                    content.append(imagen)
                except Exception as e:
                    content.append(Paragraph(f"Error al cargar la imagen: {str(e)}", styles['Normal']))
            else:
                content.append(Paragraph("Sin imagen disponible", styles['Normal']))

            # Agregar el precio
            content.append(Paragraph(f"Precio: {producto.precio}", styles['Normal']))

            # Agregar las especificaciones si existen
            if producto.especificaciones:
                content.append(Paragraph(f"Especificaciones: {producto.especificaciones}", styles['Normal']))

            # Agregar un espacio entre productos
            content.append(Spacer(1, 12))

        # Agregar el contenido al documento
        doc.build(content)

        # Obtener el valor del buffer
        pdf = buffer.getvalue()
        buffer.close()

        # Crear una respuesta HTTP con el contenido del PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="catalogo_productos_categoria_{categoria_id}.pdf"'
        response.write(pdf)

        return response

    except Exception as e:
        return HttpResponse(f'Error en la vista: {str(e)}', status=500)


# En venta masiva #####################################################
# ESTA RENDERIZANDO

from django.shortcuts import render
from django.http import JsonResponse
from .models import Producto, Existencia

def venta_masiva(request):
        usuario = request.session.get('usuario')  # Obtener el nombre de usuario de la sesión

        return render(request, 'venta_masiva.html', {'usuario': usuario})



from django.http import JsonResponse
from django.views.generic import View
from .models import Producto

class AutocompleteProductos(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('term', '')  # Obtener el término de búsqueda desde la URL
        
        # Filtrar productos por nombre, descripción, código o cualquier otro campo relevante
        productos = Producto.objects.filter(nombre__icontains=query) | \
                    Producto.objects.filter(descripcion__icontains=query) | \
                    Producto.objects.filter(codigo__icontains=query)

        # Crear una lista de resultados con los campos necesarios
        results = [{
            'label': f"{producto.nombre} - {producto.descripcion}",
            'value': producto.codigo,
            'stock': producto.stock,
        } for producto in productos]

        return JsonResponse(results, safe=False)
    
# Visa que maneja el detalle

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Producto, Existencia

def detalle_producto(request, codigo):
    producto = get_object_or_404(Producto, codigo=codigo)
    existencias = Existencia.objects.filter(producto=producto, estado='Disponible')

    # Preparar los detalles para enviar al frontend
    detalles = {
        'codigo': codigo,
        'nombre': producto.nombre,
        'precio': float(producto.precio),  # Convertir Decimal a float para JsonResponse
        'impuesto': 0.13,  # Ajustar según la lógica real para calcular el impuesto
        'existencias': []
    }

    # Recorrer todas las existencias del producto para agregarlas a detalles
    for existencia in existencias:
        detalle_existencia = {
            'ubicacion': existencia.ubicacion if existencia.ubicacion else '',  # Manejo de ubicaciones vacías
            'numeros_serie': existencia.numero_serie if existencia.numero_serie else '',  # Manejo de números de serie vacíos
        }
        detalles['existencias'].append(detalle_existencia)

    return JsonResponse(detalles)



# Cliente, Aqui manejamos la creacion del CLIENTE



from django.shortcuts import render
from tienda.ProductoForm import ClienteForm

def cliente_view(request):
    mensaje = None  # Variable para almacenar el mensaje de éxito o error, si es necesario

    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            mensaje = 'Cliente registrado exitosamente.'  # Mensaje de éxito
            form = ClienteForm()  # Limpiar el formulario después de guardar

    else:
        form = ClienteForm()

    return render(request, 'cliente.html', {'form': form, 'mensaje': mensaje})

# Lista de clientes:
def lista_clientes(request):
    clientes = Cliente.objects.all()  # Consulta para obtener todos los clientes
    return render(request, 'lista_clientes.html', {'clientes': clientes})



import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db import transaction
from tienda.frmvm import VentaForm
from .models import Venta, DetalleVenta, Cliente, Producto, Existencia

def procesamiento_ventamasiva(request):
    usuario = request.session.get('usuario')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print('Datos recibidos:', data)  # Verifica que los datos lleguen correctamente

            cliente_nombre = data.get('cliente_nombre')
            documentoCliente = data.get('documentoCliente')
            direccionCliente = data.get('direccionCliente')
            tipo_operacion = data.get('tipo_operacion')
            departamento = data.get('departamento')
            municipio = data.get('municipio')
            registro = data.get('registro')
            giro = data.get('giro')
            metodoPago = data.get('metodoPago')  # Asegúrate de que el nombre coincida con el JSON
            condicionesPago = data.get('condicionesPago')
            detalles_venta = data.get('detalles_venta')
            
            
       
            

            # Print values to verify they are correct
            print(f"Tipo de Operación: {tipo_operacion}")
            print(f"Departamento: {departamento}")
            print(f"Municipio: {municipio}")
            print(f"Registro: {registro}")
            print(f"Giro: {giro}")
            print(f"Método de Pago: {metodoPago}")
            print(f"Condiciones de Pago: {condicionesPago}")

            # Crear la instancia de Venta
            with transaction.atomic():
                # Buscar cliente por nombre
                cliente, creado = Cliente.objects.get_or_create(nombre=cliente_nombre.strip())

                venta = Venta.objects.create(
                    cliente=cliente,
                    documentocliente=documentoCliente,
                    direccioncliente=direccionCliente,
                    tipo_operacion=tipo_operacion,
                    departamento=departamento,
                    municipio=municipio,
                    registro=registro,
                    giro=giro,
                    metodo_pago=metodoPago,  # Asegúrate de que este campo está bien definido en tu modelo
                    condicionesPago=condicionesPago,
                    estado='Completado',
                    total=0.0,
                    vendedor = usuario
                )

                # Procesar cada detalle de venta
                for detalle in detalles_venta:
                    if 'codigo' not in detalle or 'cantidad' not in detalle or 'precio_unitario' not in detalle:
                        return JsonResponse({'error': 'Falta algún campo necesario en los detalles de venta.'}, status=400)

                    codigo_producto = detalle['codigo']
                    cantidad = detalle['cantidad']
                    precio_unitario = detalle['precio_unitario']
                    impuesto = detalle.get('impuesto', 0)
                    series_vendidas = detalle.get('numeros_serie', [])

                    # Obtener el producto por su código
                    producto = Producto.objects.get(codigo=codigo_producto)

                    # Verificar si hay suficiente stock
                    if cantidad > producto.stock:
                        return JsonResponse({'error': f"No hay suficiente stock para el producto {producto.nombre}"}, status=400)

                    # Crear un detalle por cada serie vendida
                    for serie in series_vendidas:
                        detalle_venta = DetalleVenta.objects.create(
                            venta=venta,
                            producto=producto,
                            cantidad=1,  # Cada serie vendida cuenta como una unidad
                            precio_unitario=precio_unitario,
                            impuesto=impuesto,
                            series_vendidas=serie  # Aquí se guarda una serie individual
                        )

                        # Actualizar el estado de las existencias a "Vendido"
                        existencia = Existencia.objects.get(numero_serie=serie)
                        existencia.id_venta = venta.id  # Asigna el id de la venta a id_venta en Existencia
                        existencia.venta = venta
                        existencia.estado = 'Vendido'
                        existencia.save()

                    # Restar el stock del producto vendido
                    producto.stock -= len(series_vendidas)
                    producto.save()

                    # Actualizar el stock del producto (si es necesario, dependiendo de la lógica en tu modelo Producto)
                    producto.update_stock()

                    # Log each detail saved
                    print(f"Detalle guardado para producto {producto.nombre}")

                venta.total = venta.total_venta()  # Asegúrate de que esta función calcula correctamente el total
                venta.save()
                
               
            
            
            # Devuelve el ID de la venta para que el cliente pueda redirigir
           

            
            # Devuelve el ID de la venta para que el cliente pueda redirigir
            return JsonResponse({'mensaje': 'Venta procesada exitosamente.', 'venta_id': venta.id})
          
        
        

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos JSON inválidos.'}, status=400)
        except Cliente.DoesNotExist:
            return JsonResponse({'error': 'Cliente no encontrado.'}, status=400)
        except Producto.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado.'}, status=400)
        except Existencia.DoesNotExist:
            return JsonResponse({'error': 'Existencia no encontrada.'}, status=400)
        except Exception as e:
            # Print the exception to debug
            print(f"Error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)
    
    # Reporte de ventas
    
from django.shortcuts import render
from .models import Venta

def reporte_ventas(request):
    ventas = Venta.objects.all()

    # Verificación rápida de datos
    for venta in ventas:
        print(f"Venta ID: {venta.id}")
        for detalle in venta.detalleventa_set.all():
            print(f"Detalle - Producto: {detalle.producto.nombre}, Cantidad: {detalle.cantidad}, Series: {detalle.series_vendidas}")

    return render(request, 'reporteventas.html', {'ventas': ventas})



# Generacion de la factura

from django.shortcuts import render, get_object_or_404
from .models import Venta

def crear_factura(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = venta.detalles.all()  # Obtener todos los detalles de la venta, ajusta según tu modelo

    return render(request, 'crear_factura.html', {'venta': venta, 'detalles': detalles})



# Manejo de nuevos inventarios

# views.py
from django.shortcuts import render
from .models import Producto, Existencia, Proveedor, Sucursal

def inventario_productos(request):
    productos = Producto.objects.all().prefetch_related('existencia_set')
    
    inventario_list = []
    for producto in productos:
        existencias = producto.existencia_set.all()
        for existencia in existencias:
            inventario_list.append({
                'nombre': producto.nombre,
                'codigo': producto.codigo,
                 'stock': 1, 
                'precio_unitario': producto.precio,
                'ubicacion': existencia.ubicacion,
                'proveedor': existencia.nombreProveedor,
                'fecha_ingreso': existencia.fechaIngreso,  # Añadir fecha de ingreso
                'numero_serie': existencia.numero_serie,  # Añadir número de serie
                'lote': existencia.lote,  # Añadir lote
                'nfacturaCompra': existencia.nfacturaCompra,  # Añadir número de factura
                'ordenCompra': existencia.ordenCompra,  # Añadir orden de compra
                'operador': existencia.operador,  # Añadir orden de compra
            })
    
    return render(request, 'inventario_productos.html', {'inventario': inventario_list})



# Proveedores

# En views.py

from django.shortcuts import render, redirect
from .forms import ProveedorForm

def ingresar_proveedor(request):
    mensaje = None  # Variable para almacenar el mensaje de éxito

    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            mensaje = 'Proveedor guardado con éxito.'  # Mensaje de éxito después de guardar
            form = ProveedorForm()  # Limpiar formulario para un nuevo ingreso
    else:
        form = ProveedorForm()
    
    return render(request, 'ingresar_proveedor.html', {'form': form, 'mensaje': mensaje})

# Trazabilidad series
from django.shortcuts import render
from .models import Existencia
from django.shortcuts import render, get_object_or_404

def trazabilidad_series(request):
    if request.method == 'GET':
        q = request.GET.get('q', None)  # Obtener el número de serie desde la URL
        
        if q:
            try:
                existencia = Existencia.objects.get(numero_serie=q)
                venta_asociada_id = existencia.id_venta
                
                if venta_asociada_id:
                    venta_asociada = get_object_or_404(Venta, id=venta_asociada_id)
                    detalles_venta = DetalleVenta.objects.filter(venta=venta_asociada)
                     # Obtener la fecha de la venta asociada
                    fecha_venta = venta_asociada.fecha
                    
                    context = {
                        'serie': q,
                        'venta_asociada': venta_asociada,
                        'detalles_venta': detalles_venta,
                        'fecha_venta': fecha_venta,
                    }
                    
                    return render(request, 'trazabilidad_series.html', context)
                else:
                    return render(request, 'trazabilidad_series.html', {'error': f'No se encontró una venta asociada para la serie "{q}".'})
                
            except Existencia.DoesNotExist:
                return render(request, 'trazabilidad_series.html', {'error': f'La serie "{q}" no existe en la base de datos.'})
        
        return render(request, 'trazabilidad_series.html', {'error': 'Ingrese un número de serie para buscar la trazabilidad.'})
    
    
    
   # USUARIOS
   
from django.shortcuts import render, redirect
from .forms import UsuarioForm

def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')  # Redirige a la página de inicio o donde desees
    else:
        form = UsuarioForm()
    
    return render(request, 'registrar_usuario.html', {'form': form})


# views.py

from django.shortcuts import render, redirect
from .models import Usuario
from .forms import LoginForm

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Buscar el usuario en la base de datos por username y contraseña
            try:
                user = Usuario.objects.get(nombre=username, password=password)
            except Usuario.DoesNotExist:
                user = None
            
            if user is not None:
                # Usuario encontrado, iniciar sesión
                request.session['usuario'] = user.nombre  # Guardar el nombre del usuario en la sesión
                return redirect('inicio')  # Redirigir a la página de inicio
            else:
                form.add_error(None, 'Credenciales inválidas')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

# Salir

from django.shortcuts import redirect

def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('login')


#Stock por Ubucacion
from django.shortcuts import render
from .models import Existencia

def stock_view(request):
    existencias = Existencia.objects.select_related('producto').order_by('ubicacion').all()

    context = {
        'existencias': existencias,
    }
    return render(request, 'stock.html', context)



from django.shortcuts import render
from .models import Producto

def stock_grupal(request):
    # Obtener todos los productos
    productos = Producto.objects.all().values('nombre', 'codigo', 'precio', 'stock')

    context = {
        'productos': productos,
    }

    return render(request, 'stock_grupal.html', context)





# Detalles venta modal

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Venta

def detalles_venta_modal(request, venta_id):
    venta = get_object_or_404(Venta, pk=venta_id)
    data = {
        'id': venta.id,
        'vendedor': venta.vendedor,
        'fecha': venta.fecha.strftime('%Y-%m-%d'),  # Formato de fecha deseado
        'total': venta.total,
        'tipo_operacion': venta.get_tipo_operacion_display(),  # Obtiene el nombre del tipo de operación
        
    }
    return JsonResponse(data)

#Resumen de venta
from django.shortcuts import render
from django.http import HttpResponse

def venta_resumen(request):
    # Lógica adicional aquí si es necesaria
    return render(request, 'venta_resumen.html')





from django.shortcuts import render
from django.contrib import messages
from .models import Venta

def emitir_reporte_ventas(request):
    ventas = []

    if request.method == 'POST':
        fecha_desde = request.POST.get('fecha_desde')
        fecha_hasta = request.POST.get('fecha_hasta')
        
        # Filtrar ventas por rango de fechas
        ventas = Venta.objects.filter(fecha__range=[fecha_desde, fecha_hasta])
        
        if not ventas:
            messages.warning(request, 'Lo siento, no se encontraron registros de venta en el tiempo seleccionado.')

    context = {
        'ventas': ventas
    }
    return render(request, 'venta_resumen.html', context)


