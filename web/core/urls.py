from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='home'), # La página principal del sitio
    path('shop/', views.shop_view, name='shop'),
    path('shop-detail/<int:product_id>/', views.shop_detail_view, name='shop_detail'),
    path('contact/', views.contact_view, name='contact'),
    path('testimonial/', views.testimonial_view, name='testimonial'),
    path('iniciar-pago/', views.iniciar_pago, name='iniciar_pago'),
    path('pago-exitoso/', views.pago_exitoso, name='pago_exitoso'), 
    path('pago-fallido/', views.pago_fallido, name='pago_fallido'), 
    path('pago-pendiente/', views.pago_pendiente, name='pago_pendiente'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cambiar_password/', views.cambiar_password_view, name='cambiar_password'),
    path('solicitar-reset/', views.solicitar_reset_view, name='solicitar_reset'),
    path('validar_codigo/', views.validar_codigo_view, name='validar_codigo'),
    path("registrar/", views.register_view, name="registrar"),
]