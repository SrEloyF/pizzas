# app1/views.py

from rest_framework import generics
from .models import *
from .serializers import *

class AreaListCreate(generics.ListCreateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

class CategoriaListCreate(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ClienteListCreate(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class SucursalListCreate(generics.ListCreateAPIView):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer

class PagoListCreate(generics.ListCreateAPIView):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

class PedidoListCreate(generics.ListCreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class ProductoVentaListCreate(generics.ListCreateAPIView):
    queryset = ProductoVenta.objects.all()
    serializer_class = ProductoVentaSerializer

class ProductoPrimaListCreate(generics.ListCreateAPIView):
    queryset = ProductoPrima.objects.all()
    serializer_class = ProductoPrimaSerializer

class DetallePedidoListCreate(generics.ListCreateAPIView):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer

class PaqueteListCreate(generics.ListCreateAPIView):
    queryset = Paquete.objects.all()
    serializer_class = PaqueteSerializer

class EmpleadoListCreate(generics.ListCreateAPIView):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

class HistorialListCreate(generics.ListCreateAPIView):
    queryset = Historial.objects.all()
    serializer_class = HistorialSerializer
