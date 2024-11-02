from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from api.models import *
from panel_admin.forms import *
import json
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.forms import modelform_factory
from .forms import *
from django.http import Http404
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncMonth, TruncDay, TruncHour
from django.db.models import Count, Sum, Avg
import locale

@login_required(login_url='/panel_admin/login/')
def vista_admin_ventas(request):
    #ultimos 12 meses
    hoy = timezone.now()
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    hace_12_meses = hoy - timedelta(days=365)
    ventas_mensuales = (
        Pedido.objects
        .filter(fecha_pedido__gte=hace_12_meses)
        .annotate(mes=TruncMonth('fecha_pedido'))
        .values('mes')
        .annotate(total_ventas=Count('id'))
        .order_by('mes')
    )
    meses = [(hoy - timedelta(days=30 * i)).strftime("%B %Y") for i in range(11, -1, -1)]
    data_ventas = []
    for mes in meses:
        total = next((venta['total_ventas'] for venta in ventas_mensuales if venta['mes'].strftime("%B %Y") == mes), 0)
        data_ventas.append(total)

    #metodos pagos
    metodos_pago = Pago.objects.values('metodo_pago').annotate(cantidad=Count('id'))
    data_pagos = [{pago['metodo_pago']: pago['cantidad']} for pago in metodos_pago]

    #top dias
    top_dias = Pedido.objects \
        .annotate(dia=TruncDay('fecha_pedido')) \
        .values('dia') \
        .annotate(total_ventas=Count('id')) \
        .order_by('-total_ventas')[:4]

    top_dias_data = [{"dia": dia['dia'].strftime('%A'), "total_ventas": dia['total_ventas']} for dia in top_dias]

    # Horas con más ventas (Top 4) 
    top_horas = Pedido.objects \
        .annotate(hora=TruncHour('fecha_pedido')) \
        .values('hora') \
        .annotate(total_ventas=Count('id')) \
        .order_by('-total_ventas')[:4]

    top_horas_data = [{"hora": hora['hora'].strftime('%H:%M'), "total_ventas": hora['total_ventas']} for hora in top_horas]

    # Ingresos del mes actual
    inicio_mes = timezone.now().replace(day=1)
    fin_mes = inicio_mes + timedelta(days=31)
    ingresos_mes = Pago.objects.filter(pedido__fecha_pedido__range=(inicio_mes, fin_mes)).aggregate(Sum('monto'))['monto__sum'] or 0

    # Costo promedio de venta
    costo_promedio_venta = Pago.objects.aggregate(Avg('monto'))['monto__avg'] or 0

    return render(request, 'panel_admin/admin_ventas.html', {
        'data_ventas': json.dumps(data_ventas),
        'data_pagos': json.dumps(data_pagos),
        'meses': json.dumps(meses),
        'top_dias_data': top_dias_data,
        'top_horas_data': top_horas_data,
        'ingresos_mes': ingresos_mes,
        'costo_promedio_venta': costo_promedio_venta,
    })


@login_required(login_url='/panel_admin/login/')
def vista_admin_empleados(request):
    return render(request, 'panel_admin/admin_empleados.html')

@login_required(login_url='/panel_admin/login/')
def vista_admin_plantilla(request):
    return render(request, 'panel_admin/admin_base.html')

@login_required(login_url='/panel_admin/login/')
def vista_admin_sucursales(request):
    return render(request, 'panel_admin/admin_sucursales.html')

@login_required(login_url='/panel_admin/login/')
def vista_admin_clientes(request):
    return render(request, 'panel_admin/admin_clientes.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['contrasena']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'admin_ventas')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'panel_admin/login.html')

class UsuarioAdminListView(LoginRequiredMixin, ListView):
    login_url = '/panel_admin/login/'
    model = UsuarioAdmin
    template_name = 'panel_admin/lista.html'
    context_object_name = 'objetos'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos'] = ['id', 'usuario', 'rol']
        context['model_name'] = "UsuarioAdmins"
        return context

class AreaListView(LoginRequiredMixin, ListView):
    login_url = '/panel_admin/login/'
    model = Area
    template_name = 'panel_admin/lista.html'
    context_object_name = 'objetos'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos'] = ['id', 'nombre_area', 'descripcion']
        context['model_name'] = "Areas"
        return context

class CategoriaListView(LoginRequiredMixin, ListView):
    login_url = '/panel_admin/login/'
    model = Categoria
    template_name = 'panel_admin/lista.html'
    context_object_name = 'objetos'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos'] = ['id', 'nombre', 'descripcion']
        context['model_name'] = "Categorias"
        return context

class SucursalListView(LoginRequiredMixin, ListView):
    login_url = '/panel_admin/login/'
    model = Sucursal
    template_name = 'panel_admin/lista.html'
    context_object_name = 'objetos'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos'] = ['id', 'telefono', 'direccion', 'hora_inicio', 'hora_cierre']
        context['model_name'] = "Sucursales"
        return context

class EmpleadoListView(LoginRequiredMixin, ListView):
    login_url = '/panel_admin/login/'
    model = Empleado
    template_name = 'panel_admin/lista.html'
    context_object_name = 'objetos'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos'] = ['id', 'sucursal', 'area', 'nombre', 'apellido', 'cargo', 'estado']
        context['model_name'] = "Empleados"
        return context

class ProductoVentaListView(LoginRequiredMixin, ListView):
    login_url = '/panel_admin/login/'
    model = ProductoVenta
    template_name = 'panel_admin/lista.html'
    context_object_name = 'objetos'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos'] = ['id', 'nombre', 'precio', 'descripcion', 'imagen']
        context['model_name'] = "ProductosVenta"
        return context

class ProductoPrimaListView(LoginRequiredMixin, ListView):
    login_url = '/panel_admin/login/'
    model = ProductoPrima
    template_name = 'panel_admin/lista.html'
    context_object_name = 'objetos'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos'] = ['id', 'categoria', 'nombre', 'precio', 'descripcion', 'imagen']
        context['model_name'] = "ProductosPrima"
        return context

class PaqueteListView(LoginRequiredMixin, ListView):
    login_url = '/panel_admin/login/'
    model = Paquete
    template_name = 'panel_admin/lista.html'
    context_object_name = 'objetos'
    paginate_by = 8 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos'] = ['id', 'proventa', 'proprima']
        context['model_name'] = "Paquetes"
        return context

################################
class ModelFactory:
    models_forms = {
        'areas': (Area, AreaForm),
        'categorias': (Categoria, CategoriaForm),
        'sucursales': (Sucursal, SucursalForm),
        'empleados': (Empleado, EmpleadoForm),
        'productosventa': (ProductoVenta, ProductoVentaForm),
        'productosprima': (ProductoPrima, ProductoPrimaForm),
        'paquetes': (Paquete, PaqueteForm),
        'usuarioadmins': (UsuarioAdmin, UsuarioAdminForm)
    }

    @classmethod
    def get_model_and_form(cls, model_name):
        return cls.models_forms.get(model_name)

class BaseObjetoView:
    template_name = 'panel_admin/aniadir_editar.html'

    def get_model(self):
        model_name = self.kwargs['model_name']
        model_and_form = ModelFactory.get_model_and_form(model_name)
        if not model_and_form:
            raise Http404(f"Modelo {model_name} no encontrado.")
        return model_and_form

    def get_form_class(self):
        _, form_class = self.get_model()
        return form_class

    def get_success_url(self):
        model_name = self.kwargs["model_name"]
        return reverse_lazy(f'{model_name}_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.kwargs['model_name']
        return context

class CrearObjetoView(BaseObjetoView, CreateView):
    pass

class EditarObjetoView(BaseObjetoView, UpdateView):
    def get_object(self):
        model, _ = self.get_model()
        return get_object_or_404(model, pk=self.kwargs['pk'])


class EliminarObjetoView(BaseObjetoView, DeleteView):
    template_name = '' 

    def get_object(self):
        model, _ = self.get_model()
        return get_object_or_404(model, pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, 'Registro eliminado exitosamente.')
        except IntegrityError:
            messages.error(request, 'No se puede eliminar el registro porque está relacionado.')
        return redirect(self.get_success_url())
