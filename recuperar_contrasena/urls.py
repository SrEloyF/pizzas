from django.urls import path
from .views import *
from django.conf.urls.static import static

urlpatterns = [
    path('solicitar-recuperacion/', SolicitarRecuperacionContrasena.as_view(), name='solicitar_recuperacion'),
    path('restablecer-contrasena/<int:cliente_id>/<str:token>/', RestablecerContrasena.as_view(), name='restablecer_contrasena'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)