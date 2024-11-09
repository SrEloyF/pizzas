from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from rest_framework.authtoken import views

model_views = {
    'areas': AreaListCreate,
    'categorias': CategoriaListCreate,
    'clientes': ClienteListCreateUpdate,
    'sucursales': SucursalListCreate,
    'pagos': PagoListCreate,
    'pedidos': PedidoListCreate,
    'productos-venta': ProductoVentaListCreate,
    'productos-prima': ProductoPrimaListCreate,
    'detalles-pedido': DetallePedidoListCreate,
    'paquetes': PaqueteListCreate,
    'empleados': EmpleadoListCreate,
    'historiales': HistorialListCreate,
    'repertorios': RepertorioListCreate,
}

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('clientes/<int:pk>/', ClienteListCreateUpdate.as_view(), name='clientes-list-create-update'),
] + [path(f'{key}/', view.as_view(), name=f'{key}-list-create') for key, view in model_views.items()]