from rest_framework import generics
from .models import *
from .serializers import *

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import *

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

    def put(self, request):
        return None

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


class EncryptPasswordView(APIView):
    def post(self, request):
        password = request.data.get("password")
        if not password:
            return Response({"error": "Password not provided"}, status=status.HTTP_400_BAD_REQUEST)
        hashed_password = make_password(password)
        return Response({"hashed_password": hashed_password}, status=status.HTTP_200_OK)

class CheckPasswordView(APIView):
    def post(self, request):
        password = request.data.get("password")
        hashed_password = request.data.get("hashed_password")
        
        if not password or not hashed_password:
            return Response({"error": "Password or hash not provided"}, status=status.HTTP_400_BAD_REQUEST)
        password_is_correct = check_password(password, hashed_password)
        
        if password_is_correct:
            return Response({"message": "Password is correct"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        
class RegistroView(APIView):
    def post(self, request):
        serializer = ClienteSerializer(data=request.data.copy())
        if serializer.is_valid():
            cliente = serializer.save()
            
            tokens = get_tokens_for_user(cliente)
            response = Response({"detail": "Usuario registrado exitosamente"}, status=status.HTTP_201_CREATED)
            
            response.set_cookie(
                key='access_token',
                value=tokens['access'],
                httponly=True,
                secure=True,
                max_age=60*5,
                samesite='Lax'
            )
            response.set_cookie(
                key='refresh_token',
                value=tokens['refresh'],
                httponly=True,
                secure=True,
                max_age=60*60*24*7,
                samesite='Lax'
            )

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        usuario = request.data.get('USUARIO')
        contrasena = request.data.get('CONTRASENA')
        
        try:
            cliente = Cliente.objects.get(USUARIO=usuario)
        except Cliente.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        if check_password(contrasena,cliente.contrasena):
            refresh = RefreshToken.for_user(cliente)
            access = refresh.access_token
            
            response = Response({'detail':'inicio de sesión exitoso'},status=status.HTTP_200_OK)
    
            response.set_cookie(
                key='access_token',
                value=str(access),
                httponly=True,
                secure=True,
                # max_age=60*60*1,
                max_age=60*4,
                samesite='Lax',
            )
            
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=True,
                max_age=60*60*24*7,
                samesite='Lax',
            )
            
            return response
        else:
            return Response({'detail': 'Credenciales incorrectas'}, status=status.HTTP_401_UNAUTHORIZED)

class RefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        
        if refresh_token:
            request.data['refresh'] = refresh_token
            
            response = super().post(request, *args, **kwargs)
            
            if response.status_code == 200:
                new_access_token = response.data.get('access', None)
                # new_refresh_token = response.data.get('refresh', None)
                
                # print(new_refresh_token)
                if new_access_token:
                    response.delete_cookie('access_token')
                    # response.delete_cookie('refresh_token')
                    
                    response.set_cookie(
                        key='access_token',
                        value=new_access_token,
                        httponly=True,
                        secure=True,
                        max_age=60*4,
                        samesite='Lax'
                    )
                    
                    response.data = {'message': 'Access Token refreshed successfully'}
                else:
                    response.data = {'detail': 'New tokens not found in response'}
                    response.status_code = status.HTTP_400_BAD_REQUEST

            return response
        else:
            return Response({"detail": "Refresh token not found"}, status=status.HTTP_400_BAD_REQUEST)

def get_tokens_for_user(cliente):
    refresh = RefreshToken.for_user(cliente)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }