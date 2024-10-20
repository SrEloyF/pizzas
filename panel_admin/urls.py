from django.urls import path
from . import views

urlpatterns = [
    path('ventas/', views.vista_admin_ventas, name='admin_ventas'),
    path('empleados/', views.vista_admin_empleados, name='admin_empleados'),
    path('plantilla/', views.vista_admin_plantilla, name='admin_plantilla'),
]