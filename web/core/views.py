import requests

from django.shortcuts import render, redirect

def index_view(request):
    return render(request, 'core/index.html') # El nombre es 'core/index.html' por la estructura

def shop_view(request):
    return render(request, 'core/shop.html')

def shop_detail_view(request, product_id): # Ejemplo para shop-detail.html
    api_host = "ferremas-api2" # <--- ¡CAMBIA 'api' POR EL NOMBRE REAL DE TU SERVICIO SPRING BOOT!
    api_port = "8080" # Puerto en el que tu API de Spring Boot está escuchando DENTRO de su contenedor

    api_url = f"http://{api_host}:{api_port}/productos/{product_id}"

    product = None
    error_message = None
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Lanza un error si la respuesta no es exitosa
        product = response.json()  # Convierte la respuesta JSON a un diccionario de Python
    except requests.exceptions.RequestException as e:
        error_message = f"Error al obtener el producto: {e}"
        print(f"Debug: {error_message}")
    except ValueError as e:
        error_message = f"Error al procesar la respuesta: {e}"
        print(f"Debug: {error_message}")

    if product is None:
        context = {
            'product': None, # No hay producto
            'error_message': error_message if error_message else "Producto no encontrado o error al cargar los datos."
        }
    else:
        context = {
            'product': product,  # Producto obtenido de la API
            'error_message': None  # No hay error
        }
    return render(request, 'core/shop-detail.html', context)

def cart_view(request):
    return render(request, 'core/cart.html')

def checkout_view(request): # Si esta es la plantilla de pago principal ahora
    return render(request, 'core/checkout.html')

def contact_view(request):
    return render(request, 'core/contact.html')

def testimonial_view(request):
    return render(request, 'core/testimonial.html')

def page_not_found_view(request, exception):
    return render(request, 'core/404.html', status=404)

