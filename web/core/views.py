import requests
import mercadopago

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from collections import defaultdict

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

def panel_admin_inicio(request):
    # Obtener usuarios
    try:
        response_usuarios = requests.get("http://ferremas-api1:8000/clientes/")
        response_usuarios.raise_for_status()
        usuarios = response_usuarios.json()
    except requests.RequestException:
        usuarios = []

    # Obtener productos
    try:
        response_productos = requests.get("http://ferremas-api2:8080/productos")
        response_productos.raise_for_status()
        productos = response_productos.json()
    except requests.RequestException:
        productos = []

    # Obtener pagos
    try:
        response_pagos = requests.get("http://ferremas-api1:8000/pagos")
        response_pagos.raise_for_status()
        pagos = response_pagos.json()
    except requests.RequestException:
        pagos = []

    # Contar pagos pendientes
    pagos_pendientes = len([p for p in pagos if p.get("estado_pago", "").lower() == "pendiente"])

    # Procesar productos por categoría
    productos_por_categoria = {}
    productos_sin_imagen = 0

    for producto in productos:
        # Validar si tiene imagen
        if not producto.get("imagenUrl"):
            productos_sin_imagen += 1

        # Contar productos por categoría
        categoria = producto.get("categoriaNombre")
        if categoria:
            productos_por_categoria[categoria] = productos_por_categoria.get(categoria, 0) + 1
        else:
            productos_por_categoria["Sin categoría"] = productos_por_categoria.get("Sin categoría", 0) + 1

    productos_categoria_list = [
        {"categoria": cat, "cantidad": cant}
        for cat, cant in productos_por_categoria.items()
    ]

    #Procesar productos por marca
    productos_por_marca = {}

    for producto in productos:
        marca = producto.get("marcaNombre")
        if marca:
            productos_por_marca[marca] = productos_por_marca.get(marca, 0) + 1
        else:
            productos_por_marca["Sin marca"] = productos_por_marca.get("Sin marca", 0) + 1

    productos_marca_list = [
        {"marca": marca, "cantidad": cant}
        for marca, cant in productos_por_marca.items()
    ]

    return render(request, "core/panel_admin.html", {
        "total_usuarios": len(usuarios),
        "ultimos_usuarios": sorted(usuarios, key=lambda x: x.get("id_usuario", 0), reverse=True)[:5],
        "total_productos": len(productos),
        "productos_sin_imagen": productos_sin_imagen,
        "productos_categoria_json": json.dumps(productos_categoria_list),
        "productos_marca_json": json.dumps(productos_marca_list),
        "pagos_pendientes": pagos_pendientes,
        
    })

def admin_listado_usuarios(request):
    try:
        response = requests.get("http://ferremas-api1:8000/clientes/")
        if response.status_code == 200:
            usuarios = response.json()
        else:
            usuarios = []
            messages.error(request, "Error al obtener los usuarios.")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        usuarios = []
        messages.error(request, "No se pudo conectar con el servidor.")

    return render(request, "core/usuarios.html", {"usuarios": usuarios})

def admin_registrar_usuario(request):
    if request.method == "POST":
        rut = request.POST.get("rut")
        nombre = request.POST.get("nombre")
        apellido_p = request.POST.get("apellido_p")
        apellido_m = request.POST.get("apellido_m")
        snombre = request.POST.get("snombre")
        email = request.POST.get("email")
        fono = request.POST.get("fono")
        direccion = request.POST.get("direccion")
        password = request.POST.get("password")
        rol_id = request.POST.get("rol_id")  

        try:
            response = requests.post(
                "http://ferremas-api1:8000/clientes/",
                params={
                    "rut": rut,
                    "nombre": nombre,
                    "apellido_p": apellido_p,
                    "apellido_m": apellido_m,
                    "snombre": snombre,
                    "email": email,
                    "fono": fono,
                    "direccion": direccion,
                    "password": password,
                    "rol_id": rol_id,
                    "requiere_cambio_password": 0
                }
            )
            if response.status_code == 200:
                messages.success(request, "Usuario registrado exitosamente.")
                return redirect("admin_listado_usuarios")
            elif response.status_code == 409:
                messages.error(request, "El email ya está registrado.")
            else:
                messages.error(request, f"Error al registrar: {response.json().get('detail')}")
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API: {e}")
            messages.error(request, "Error al conectar con el servidor. Inténtalo más tarde.")

    return render(request, "core/registro_usuarios.html")


def admin_editar_usuario(request, usuario_id):
    try:
        # Obtener datos actuales del usuario desde la API
        response = requests.get(f"http://ferremas-api1:8000/clientes/{usuario_id}")
        if response.status_code == 200:
            usuario = response.json()
        else:
            messages.error(request, "No se pudo obtener la información del usuario.")
            return redirect("admin_listado_usuarios")
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        messages.error(request, "Error al conectar con el servidor.")
        return redirect("admin_listado_usuarios")

    if request.method == "POST":
        # Recoger datos del formulario
        rut = request.POST.get("rut")
        nombre = request.POST.get("nombre")
        apellido_p = request.POST.get("apellido_p")
        apellido_m = request.POST.get("apellido_m")
        snombre = request.POST.get("snombre")
        email = request.POST.get("email")
        fono = request.POST.get("fono")
        direccion = request.POST.get("direccion")
        password = request.POST.get("password")  # Puede venir vacío
        rol_id = request.POST.get("rol_id")

        # Crear dict con los datos actualizados
        datos_actualizados = {
            "rut": rut,
            "nombre": nombre,
            "apellido_p": apellido_p,
            "apellido_m": apellido_m,
            "snombre": snombre,
            "email": email,
            "fono": fono,
            "direccion": direccion,
            "rol_id": rol_id
        }

        # Solo se incluye password si fue modificado
        if password:
            datos_actualizados["password"] = password

        try:
            patch_response = requests.patch(
                f"http://ferremas-api1:8000/clientes/{usuario_id}",
                params=datos_actualizados
            )
            if patch_response.status_code == 200:
                messages.success(request, "Usuario actualizado correctamente.")
                return redirect("admin_listado_usuarios")
            else:
                messages.error(request, f"Error al actualizar usuario: {patch_response.json().get('detail')}")
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API: {e}")
            messages.error(request, "Error al conectar con el servidor.")

    return render(request, "core/editar_usuario.html", {"usuario": usuario})

def admin_eliminar_usuario(request, usuario_id):
    try:
        response = requests.delete(f"http://ferremas-api1:8000/clientes/{usuario_id}")
        if response.status_code == 200:
            messages.success(request, "Usuario eliminado exitosamente.")
        elif response.status_code == 404:
            messages.error(request, "Usuario no encontrado.")
        else:
            messages.error(request, f"Error al eliminar usuario: {response.text}")
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error al conectar con la API: {e}")

    return redirect("admin_listado_usuarios")

def admin_cambiar_rol(request, usuario_id):
    if request.method == "POST":
        nuevo_rol = request.POST.get("rol_id")
        try:
            response = requests.patch(
                f"http://ferremas-api1:8000/clientes/{usuario_id}",
                params={"rol_id": nuevo_rol}
            )
            if response.status_code == 200:
                messages.success(request, "Rol actualizado correctamente.")
            else:
                messages.error(request, f"Error al actualizar rol: {response.text}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Error al conectar con la API: {e}")

        return redirect("admin_listado_usuarios")

def admin_cambiar_rol(request, usuario_id):
    if request.method == "POST":
        nuevo_rol = request.POST.get("rol_id")
        try:
            response = requests.patch(
                f"http://ferremas-api1:8000/clientes/{usuario_id}",
                params={"rol_id": nuevo_rol}
            )
            if response.status_code == 200:
                messages.success(request, "Rol actualizado correctamente.")
            else:
                messages.error(request, f"Error al actualizar rol: {response.text}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Error al conectar con la API: {e}")

        return redirect("admin_listado_usuarios")

    # Método GET: obtener rol del usuario
    try:
        response = requests.get(f"http://ferremas-api1:8000/clientes/{usuario_id}")
        if response.status_code == 200:
            usuario = response.json()
            return render(request, "core/cambiar_rol.html", {"usuario": usuario})
        else:
            messages.error(request, "No se pudo obtener el usuario.")
            return redirect("admin_listado_usuarios")
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error al conectar con la API: {e}")
        return redirect("admin_listado_usuarios")

def listar_productos(request):
    productos_url = "http://ferremas-api2:8080/productos"
    categorias_url = "http://ferremas-api2:8080/categorias"
    marcas_url = "http://ferremas-api2:8080/marcas"

    productos_response = requests.get(productos_url)
    categorias_response = requests.get(categorias_url)
    marcas_response = requests.get(marcas_url)

    productos = productos_response.json() if productos_response.status_code == 200 else []
    categorias = categorias_response.json() if categorias_response.status_code == 200 else []
    marcas = marcas_response.json() if marcas_response.status_code == 200 else []
    print("=== DEBUG PRODUCTOS ===")
    for idx, p in enumerate(productos):
        print(f"[{idx}] => {p}")

    # Filtros
    nombre_filtro = request.GET.get("nombre", "").lower()
    categoria_filtro = request.GET.get("categoria", "")
    marca_filtro = request.GET.get("marca", "")

    productos_filtrados = []

    for p in productos:
        try:
            nombre_ok = nombre_filtro in p["nombre"].lower() if nombre_filtro else True
            categoria_ok = p.get("categoriaNombre") == categoria_filtro if categoria_filtro and categoria_filtro != "todos" else True
            marca_ok = p.get("marcaNombre") == marca_filtro if marca_filtro and marca_filtro != "todos" else True

            if nombre_ok and categoria_ok and marca_ok:
                productos_filtrados.append(p)

        except Exception as e:
            print(f"[ERROR] Producto inválido: {p}")
            print(f"[EXCEPCIÓN] {e}")

    productos = productos_filtrados


    return render(request, "core/productos.html", {
        "productos": productos,
        "categorias": categorias,
        "marcas": marcas,
        "nombre_filtro": nombre_filtro,
        "categoria_filtro": categoria_filtro,
        "marca_filtro": marca_filtro
    })


@csrf_exempt
def agregar_producto(request):
    categorias = requests.get("http://ferremas-api2:8080/categorias").json()
    marcas = requests.get("http://ferremas-api2:8080/marcas").json()

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        precio = request.POST.get("precio")
        imagenUrl = request.POST.get("imagenUrl")
        categoria_id = request.POST.get("categoria_id")
        marca_id = request.POST.get("marca_id")

        nuevo_producto = {
            "nombre": nombre,
            "descripcion": descripcion,
            "precio": precio,
            "imagenUrl": imagenUrl,
            "categoriaId": int(categoria_id),
            "marcaId": int(marca_id)
        }

        response = requests.post("http://ferremas-api2:8080/productos", json=nuevo_producto)

        if response.status_code == 200:
            messages.success(request, "Producto agregado correctamente.")
            return redirect("listar_productos")
        else:
            messages.error(request, "Error al agregar el producto. Intente nuevamente.")

    return render(request, "core/agregar_producto.html", {
        "categorias": categorias,
        "marcas": marcas
    })

@csrf_exempt
def eliminar_producto(request, producto_id):
    url = f"http://ferremas-api2:8080/productos/{producto_id}"
    response = requests.delete(url)

    if response.status_code == 200:
        messages.success(request, "Producto eliminado correctamente.")
    else:
        messages.error(request, "Error al eliminar el producto. Intente nuevamente.")

    return redirect("listar_productos")

def editar_producto(request, producto_id):
    producto_url = f"http://ferremas-api2:8080/productos/{producto_id}"
    categorias_url = "http://ferremas-api2:8080/categorias"
    marcas_url = "http://ferremas-api2:8080/marcas"

    if request.method == "GET":
        producto_response = requests.get(producto_url)
        categorias_response = requests.get(categorias_url)
        marcas_response = requests.get(marcas_url)

        if producto_response.status_code == 200:
            producto = producto_response.json()
            categorias = categorias_response.json() if categorias_response.status_code == 200 else []
            marcas = marcas_response.json() if marcas_response.status_code == 200 else []

            return render(request, "core/editar_producto.html", {
                "producto": producto,
                "categorias": categorias,
                "marcas": marcas
            })
        else:
            messages.error(request, "No se pudo obtener el producto.")
            return redirect("listar_productos")

    elif request.method == "POST":
        data = {
            "nombre": request.POST.get("nombre"),
            "descripcion": request.POST.get("descripcion"),
            "precio": request.POST.get("precio"),
            "categoriaId": int(request.POST.get("categoria")),
            "marcaId": int(request.POST.get("marca")),
            "imagenUrl": request.POST.get("imagenUrl"),
        }

        response = requests.put(producto_url, json=data)
        if response.status_code == 200:
            messages.success(request, "Producto actualizado correctamente.")
        else:
            messages.error(request, "Error al actualizar el producto.")

        return redirect("listar_productos")
    


def logout_view(request):
    request.session.flush()  # Elimina todos los datos de la sesión
    return redirect('/')  # Redirige a la página principal después del logout

def ventas(request):

    
    response = requests.get("http://ferremas-api1:8000/pagos/listar")
    if response.status_code == 200:
        pagos = response.json()
        return render(request, "core/ventas.html", {"pagos": pagos})
    else:
        messages.error(request, "Error al obtener los pagos.")
        return redirect("panel_admin_inicio")


def aprobar_venta(request, pago_id):
    print("### APROBANDO PAGO ###")  # VERIFICAR SI SE IMPRIME ESTO

    if request.method == "POST":
        contador_id = request.session.get('user', {}).get('id_usuario') # Obtener el ID del contador desde la sesión
        print("Contador ID:", contador_id)

        response = requests.patch(
            f"http://ferremas-api1:8000/pagos/aprobar/{pago_id}",
            json={
                "contador_id": contador_id,
                "estado_pago": "Aprobado" 
                }
        )

        print("STATUS:", response.status_code)
        print("RESPUESTA:", response.text)

    return redirect("ventas")


def page_not_found_view(request, exception):
    return render(request, 'core/404.html', status=404)

