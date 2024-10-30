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


@login_required(login_url='/panel_admin/login/')
def vista_admin_ventas(request):
    data = [10, 20, 30, 40, 50, 10, 20, 30, 40, 50, 23, 33]
    data_pagos = [140, 235]
    return render(request, 'panel_admin/admin_ventas.html', {
        'data': json.dumps(data),
        'data_pagos': json.dumps(data_pagos),
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
        #'superusuarios': (SuperUsuario, SuperUsuarioForm)
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
