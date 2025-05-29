import requests
import mercadopago

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render, redirect

def index_view(request):
    return render(request, 'core/index.html') # El nombre es 'core/index.html' por la estructura

def shop_view(request):
    return render(request, 'core/shop.html')

def shop_detail_view(request, product_id): # Ejemplo para shop-detail.html
    api_host = "ferremas-api2" 
    api_port = "8080" 

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

@csrf_exempt
def iniciar_pago(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)
        carrito = data.get('cart', [])

        if not carrito:
            return JsonResponse({'error': 'Carrito vacío'}, status=400)

        sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

        # Armar los ítems para la preferencia
        items = []
        for producto in carrito:
            items.append({
                "title": producto['nombre'],
                "quantity": int(producto['quantity']),
                "unit_price": float(producto['precio'])
            })

        # Construir la preferencia
        preference_data = {
            "items": items,
            "back_urls": {
                "success": "http://127.0.0.1:8001/pago-exitoso/",
                "failure": "http://127.0.0.1:8001/pago-fallido/",
                "pending": "http://127.0.0.1:8001/pago-pendiente/"
            },
        }

        # Crear la preferencia en Mercado Pago
        preference_response = sdk.preference().create(preference_data)
        print("🔎 Respuesta de Mercado Pago:", preference_response)

        if "response" in preference_response:
            response_data = preference_response["response"]
            print("✅ Campos disponibles:", response_data.keys())

            if "sandbox_init_point" in response_data:
                return JsonResponse({"init_point": response_data["sandbox_init_point"]})
            else:
                print("❌ sandbox_init_point no encontrado.")
                return JsonResponse({"error": "No se pudo generar el enlace de pago"}, status=500)
        else:
            return JsonResponse({"error": "Respuesta inválida de Mercado Pago"}, status=500)

    except Exception as e:
        print("❌ Error al crear preferencia:", str(e))
        return JsonResponse({"error": "Error interno del servidor"}, status=500)

def pago_exitoso(request):
    # Aquí puedes manejar la lógica después de un pago exitoso
    return render(request, 'core/pago_exitoso.html')

def pago_fallido(request):
    # Aquí puedes manejar la lógica después de un pago fallido
    return render(request, 'core/pago_fallido.html')

def pago_pendiente(request):
    # Aquí puedes manejar la lógica después de un pago pendiente
    return render(request, 'core/pago_pendiente.html')

def page_not_found_view(request, exception):
    return render(request, 'core/404.html', status=404)

