from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

model_views = {
    'areas': AreaListCreate,
    'categorias': CategoriaListCreate,
    'clientes': ClienteListCreate,
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
    path('logout/', LogoutView.as_view(), name='logout'),
] + [path(f'{key}/', view.as_view(), name=f'{key}-list-create') for key, view in model_views.items()]