from django.urls import path
from .views import *

urlpatterns = [
    path('areas/', AreaListCreate.as_view(), name='area-list-create'),
    path('categorias/', CategoriaListCreate.as_view(), name='categoria-list-create'),
    path('clientes/', ClienteListCreate.as_view(), name='cliente-list-create'),
    path('sucursales/', SucursalListCreate.as_view(), name='sucursal-list-create'),
    path('pagos/', PagoListCreate.as_view(), name='pago-list-create'),
    path('pedidos/', PedidoListCreate.as_view(), name='pedido-list-create'),
    path('productos-venta/', ProductoVentaListCreate.as_view(), name='producto-venta-list-create'),
    path('productos-prima/', ProductoPrimaListCreate.as_view(), name='producto-prima-list-create'),
    path('detalles-pedido/', DetallePedidoListCreate.as_view(), name='detalle-pedido-list-create'),
    path('paquetes/', PaqueteListCreate.as_view(), name='paquete-list-create'),
    path('empleados/', EmpleadoListCreate.as_view(), name='empleado-list-create'),
    path('historiales/', HistorialListCreate.as_view(), name='historial-list-create'),
]
