from django.shortcuts import redirect
from django.contrib import messages

class VerificarAccesoPanelMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar si la URL empieza con /panel/
        if request.path.startswith('/panel/'):
            user = request.session.get("user")
            # Si no hay usuario o si su rol_id es 1, redirigir al inicio
            if not user or user.get("rol_id") == 1:
                messages.error(request, "Acceso denegado: No tienes permisos para ver esa sección.")
                return redirect('/')
        return self.get_response(request)