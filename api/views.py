from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status

class ListCreateView(generics.ListCreateAPIView):
    serializer_class = None
    queryset = None

    def get_queryset(self):
        model = self.serializer_class.Meta.model
        return model.objects.all()

class AreaListCreate(ListCreateView):
    serializer_class = AreaSerializer

class CategoriaListCreate(ListCreateView):
    serializer_class = CategoriaSerializer

class ClienteListCreateUpdate(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SucursalListCreate(ListCreateView):
    serializer_class = SucursalSerializer

class PagoListCreate(ListCreateView):
    serializer_class = PagoSerializer

class PedidoListCreate(ListCreateView):
    serializer_class = PedidoSerializer

class ProductoVentaListCreate(ListCreateView):
    serializer_class = ProductoVentaSerializer

class ProductoPrimaListCreate(ListCreateView):
    serializer_class = ProductoPrimaSerializer

class DetallePedidoListCreate(ListCreateView):
    serializer_class = DetallePedidoSerializer

class PaqueteListCreate(ListCreateView):
    serializer_class = PaqueteSerializer

class EmpleadoListCreate(ListCreateView):
    serializer_class = EmpleadoSerializer

class HistorialListCreate(ListCreateView):
    serializer_class = HistorialSerializer

class RepertorioListCreate(ListCreateView):
    serializer_class = RepertorioSerializer
