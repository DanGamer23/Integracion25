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
    path("panel/", views.panel_admin_inicio, name="panel_admin_inicio"),
    path("panel/usuarios/", views.admin_listado_usuarios, name="admin_listado_usuarios"),
    path('panel/usuarios/nuevo/', views.admin_registrar_usuario, name='admin_registro_usuarios'),
    path('panel/usuarios/editar/<int:usuario_id>/', views.admin_editar_usuario, name='admin_editar_usuario'),
    path('panel/usuarios/eliminar/<int:usuario_id>/', views.admin_eliminar_usuario, name='admin_eliminar_usuario'),
    path('panel/usuarios/rol/<int:usuario_id>/', views.admin_cambiar_rol, name='admin_cambiar_rol'),
    path('panel/productos/', views.listar_productos, name='listar_productos'),
    path('panel/productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('panel/productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('panel/productos/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('panel/ventas/', views.ventas, name='ventas'),
    path('panel/ventas/aprobar/<int:pago_id>/', views.aprobar_venta, name='aprobar_venta'),
]