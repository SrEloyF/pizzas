from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from rest_framework.authtoken import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('areas/', AreaListCreate.as_view(), name='areas'),
    path('categorias/', CategoriaListCreate.as_view(), name='categorias'),
    path('clientes/', ClienteListCreateUpdate.as_view(), name='clientes'),
    path('sucursales/', SucursalListCreate.as_view(), name='sucursales'),
    path('pagos/', PagoListCreate.as_view(), name='pagos'),
    path('pedidos/', PedidoListCreate.as_view(), name='pedidos'),
    path('repertorios/', RepertorioListCreate.as_view(), name='repertorios'),
    path('productos-venta/', ProductoVentaListCreate.as_view(), name='productos-venta'),
    path('productos-prima/', ProductoPrimaListCreate.as_view(), name='productos-prima'),
    path('detalles-pedido/', DetallePedidoListCreate.as_view(), name='detalles-pedido'),
    path('paquetes/', PaqueteListCreate.as_view(), name='paquetes'),
    path('empleados/', EmpleadoListCreate.as_view(), name='empleados'),
    path('historiales/', HistorialListCreate.as_view(), name='historiales'),

    #path('enpass/', EncryptPasswordView.as_view(), name='pass'),
    #path('checkhash/', CheckPasswordView.as_view(), name='hash'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh'),

    path('api-token-auth/', views.obtain_auth_token),
    path('logout/', LogoutView.as_view(), name='logout'),


    path('solicitar-recuperacion/', SolicitarRecuperacionContrasena.as_view(), name='solicitar-recuperacion'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)