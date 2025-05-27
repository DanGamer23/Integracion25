from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def index_view(request):
    return render(request, 'core/index.html') # El nombre es 'core/index.html' por la estructura

def shop_view(request):
    return render(request, 'core/shop.html')

def shop_detail_view(request, product_id): # Ejemplo para shop-detail.html
    # Aquí eventualmente cargarías datos del producto con tu API de Spring Boot
    return render(request, 'core/shop-detail.html', {'product_id': product_id})

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