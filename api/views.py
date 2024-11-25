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

from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from .utils import cliente_token_generator
from django.shortcuts import render

class SolicitarRecuperacionContrasena(APIView):
    def post(self, request):
        correo = request.data.get("correo")
        
        if not correo:
            return Response({"error": "El correo es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cliente = Cliente.objects.get(correo=correo)
        except Cliente.DoesNotExist:
            return Response({"error": "Cliente no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        token = cliente_token_generator.make_token(cliente)
        recovery_link = f"{settings.SITE_URL}/api/restablecer-contrasena/{cliente.id_cliente}/{token}/"
        
        subject = "Recuperación de contraseña"
        html_content = f"""
        <p>Hola {cliente.usuario},</p>
        <p>Haga clic en el siguiente enlace para restablecer su contraseña:</p>
        <a href="{recovery_link}">Restablecer mi contraseña</a>
        """
        
        try:
            send_mail(
                subject,
                '',
                settings.EMAIL_HOST_USER,
                [cliente.correo],
                fail_silently=False,
                html_message=html_content
            )
            return Response({"message": "Correo de recuperación enviado."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RestablecerContrasena(APIView):
    def get(self, request, cliente_id, token):
        try:
            cliente = Cliente.objects.get(id_cliente=cliente_id)
        except Cliente.DoesNotExist:
            return Response({"error": "Cliente no encontrado."}, status=404)
        if not default_token_generator.check_token(cliente, token):
            return Response({"error": "El enlace de recuperación es inválido o ha caducado."}, status=400)
        return render(request, "api/restablecer_contrasena.html", {
            'cliente_id': cliente_id,
            'token': token
        })

    def post(self, request, cliente_id, token):
        try:
            cliente = Cliente.objects.get(id_cliente=cliente_id)
        except Cliente.DoesNotExist:
            return Response({"error": "Cliente no encontrado."}, status=404)
        if not default_token_generator.check_token(cliente, token):
            return Response({"error": "El enlace de recuperación es inválido o ha caducado."}, status=400)

        nueva_contrasena = request.POST.get("password")
        cliente.contrasena = make_password(nueva_contrasena)
        cliente.save()

        return render(request, "api/restablecer_contrasena.html", {
            'cliente_id': cliente_id,
            'token': token,
            'success_message': "Contraseña actualizada"
        })

def get_tokens_for_user(cliente):
    refresh = RefreshToken.for_user(cliente)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

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
            cliente_id = request.data.get('id_cliente')
            if not cliente_id:
                return Response({"error": "El id_cliente es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                cliente = Cliente.objects.get(id_cliente=cliente_id)
            except Cliente.DoesNotExist:
                return Response({"error": "Cliente no encontrado."}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.serializer_class(cliente, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
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


# class EncryptPasswordView(APIView):
#     def post(self, request):
#         password = request.data.get("password")
#         if not password:
#             return Response({"error": "Password not provided"}, status=status.HTTP_400_BAD_REQUEST)
#         hashed_password = make_password(password)
#         return Response({"hashed_password": hashed_password}, status=status.HTTP_200_OK)

# class CheckPasswordView(APIView):
#     def post(self, request):
#         password = request.data.get("password")
#         hashed_password = request.data.get("hashed_password")

#         if not password or not hashed_password:
#             return Response({"error": "Password or hash not provided"}, status=status.HTTP_400_BAD_REQUEST)
#         password_is_correct = check_password(password, hashed_password)

#         if password_is_correct:
#             return Response({"message": "Password is correct"}, status=status.HTTP_200_OK)
#         else:
#             return Response({"message": "Password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

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
        usuario = request.data.get('usuario')
        contrasena = request.data.get('contrasena')

        try:
            cliente = Cliente.objects.get(usuario=usuario)
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

