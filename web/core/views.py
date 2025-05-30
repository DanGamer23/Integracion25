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
        print(" Respuesta de Mercado Pago:", preference_response)

        if "response" in preference_response:
            response_data = preference_response["response"]
            print(" Campos disponibles:", response_data.keys())

            if "sandbox_init_point" in response_data:
                return JsonResponse({"init_point": response_data["sandbox_init_point"]})
            else:
                print("sandbox_init_point no encontrado.")
                return JsonResponse({"error": "No se pudo generar el enlace de pago"}, status=500)
        else:
            return JsonResponse({"error": "Respuesta inválida de Mercado Pago"}, status=500)

    except Exception as e:
        print("Error al crear preferencia:", str(e))
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

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            response = requests.post(
                'http://ferremas-api1:8000/clientes/login/',
                params={'email': email, 'password': password})
            if response.status_code == 200:
                user_data = response.json()
                request.session['user'] = user_data # Guardar datos del usuario en la sesión

                if user_data.get("rol_id") == 5 and user_data.get("requiere_cambio_password") == 1:
                    # Si el usuario es un administrador y requiere cambiar la contraseña
                    return redirect('/cambiar_password')
                
                return redirect('/')  # Redirigir a la página principal después del login exitoso
            else:
                return render(request, 'core/login.html', {'error': 'Credenciales inválidas'})
        except Exception as e:
            import traceback
            traceback.print_exc()  # Muestra la traza completa del error
            return render(request, 'core/login.html', {
                "error": f"Error al conectar con el servidor: {e}"
            })
    return render(request, 'core/login.html')

@csrf_exempt
def cambiar_password_view(request):
    user = request.session.get('user')
    if not user or user.get("rol_id") != 5:
        return redirect('/login/')
    
    if request.method == 'POST':
        nueva_password = request.POST.get('password')
        confirmar = request.POST.get('confirmar')
        if nueva_password != confirmar:
            return render(request, 'core/cambiar_password.html', {'error': 'Las contraseñas no coinciden'})
        
        # Enviar la nueva contraseña al API para actualizarla
        response = requests.post(
            'http://ferremas-api1:8000/clientes/cambiar_password/',
            json={'id_usuario': user['id_usuario'], 'nueva_password': nueva_password}
        )

        if response.status_code == 200:
            request.session['user']['requiere_cambio_password'] = 0  # Actualizar el estado en la sesión
            return redirect('/')
        else:
            return render(request, 'core/cambiar_password.html', {'error': 'Error al cambiar la contraseña'})
        
    return render(request, 'core/cambiar_password.html')

@csrf_exempt
def solicitar_reset_view(request):
    context = {}
    if request.method == "POST":
        email = request.POST.get("email")
        response = requests.post("http://ferremas-api1:8000/clientes/solicitar-reset", json={"email": email})

        if response.status_code == 200:
            codigo = response.json()["codigo"]
            request.session["reset_email"] = email
            request.session["reset_codigo"] = codigo
            context["codigo"] = codigo  
        else:
            context["error"] = f"Error: {response.status_code} - {response.text}"

    return render(request, "core/solicitar_reset.html", context)

@csrf_exempt
def validar_codigo_view(request):
    if request.method == "POST":
        codigo = request.POST.get('codigo')
        nueva_pass = request.POST.get('password')
        confirmar_pass = request.POST.get('confirmar')

        print("Código ingresado:", codigo)
        print("Nueva contraseña:", nueva_pass)
        print("Confirmación:", confirmar_pass)
        print("Código esperado:", request.session.get("reset_codigo"))

        if nueva_pass != confirmar_pass:
            print("Contraseñas no coinciden")
            return render(request, 'core/validar_codigo.html', {'error': 'Las contraseñas no coinciden'})
        
        if codigo != request.session.get("reset_codigo"):
            print("Código inválido")
            return render(request, 'core/validar_codigo.html', {'error': 'Código inválido'})

        email = request.session.get("reset_email")
        print("Email para reset:", email)

        payload = {'email': email, 'nueva_password': nueva_pass}
        print("Enviando a API1:", payload)

        response = requests.post(
            'http://ferremas-api1:8000/clientes/cambiar_password',
            json=payload
        )

        print("Respuesta API1:", response.status_code, response.text)

        if response.status_code == 200:
            print("Contraseña cambiada correctamente")
            return redirect('/login')
        else:
            print("Error en el cambio de contraseña")
            return render(request, 'core/validar_codigo.html', {
                    'error': 'Error al cambiar la contraseña',
                    'detalle': response.text 
                })

    return render(request, 'core/validar_codigo.html')

@csrf_exempt
def register_view(request):
    if request.method == "POST":
        datos = {
            "rut": request.POST.get("rut"),
            "nombre": request.POST.get("nombre"),
            "apellido_p": request.POST.get("apellido_p"),
            "apellido_m": request.POST.get("apellido_m"),
            "snombre": request.POST.get("snombre"),
            "email": request.POST.get("email"),
            "fono": request.POST.get("fono"),
            "direccion": request.POST.get("direccion"),
            "password": request.POST.get("password")
        }

        response = requests.post("http://ferremas-api1:8000/clientes/", params=datos)

        if response.status_code == 200:
            # Registro exitoso, login automático
            login_resp = requests.post(
                'http://ferremas-api1:8000/clientes/login/',
                params={'email': datos['email'], 'password': datos['password']}
            )
            if login_resp.status_code == 200:
                user_data = login_resp.json()
                request.session['user'] = user_data
                return redirect("home")  # Redirigir a la página principal después del registro exitoso
            
            return render(request, "core/login.html", {"error": "Error al iniciar sesión después del registro."})
            
        elif response.status_code == 409:
            return render(request, "core/registrar.html", {"error": "Este correo ya está registrado."})
        else:
            return render(request, "core/registrar.html", {"error": "Error al registrar. Verifica tus datos."})

    return render(request, "core/registrar.html")




def logout_view(request):
    request.session.flush()  # Elimina todos los datos de la sesión
    return redirect('/')  # Redirige a la página principal después del logout

def page_not_found_view(request, exception):
    return render(request, 'core/404.html', status=404)

