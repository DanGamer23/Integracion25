from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='home'), # La página principal del sitio
    path('shop/', views.shop_view, name='shop'),
    path('shop-detail/<int:product_id>/', views.shop_detail_view, name='shop_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'), # Tu nueva página de checkout
    path('contact/', views.contact_view, name='contact'),
    path('testimonial/', views.testimonial_view, name='testimonial'),
]