from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
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

def vista_admin_ventas(request):
    data = [10, 20, 30, 40, 50, 10, 20, 30, 40, 50, 23, 33]
    data_pagos = [140, 235]
    return render(request, 'panel_admin/admin_ventas.html', {
        'data': json.dumps(data),
        'data_pagos': json.dumps(data_pagos),
    })

def vista_admin_empleados(request):
    return render(request, 'panel_admin/admin_empleados.html')

def vista_admin_plantilla(request):
    return render(request, 'panel_admin/admin_base.html')

def vista_admin_sucursales(request):
    return render(request, 'panel_admin/admin_sucursales.html')

def vista_admin_clientes(request):
    return render(request, 'panel_admin/admin_clientes.html')


class AreaListView(ListView):
    model = Area
    template_name = 'panel_admin/lista.html'
    context_object_name = 'objetos'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos'] = ['id', 'nombre_area', 'descripcion']
        context['model_name'] = "Areas"
        return context

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'panel_admin/lista.html'
    context_object_name = 'objetos'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos'] = ['id', 'nombre', 'descripcion']
        context['model_name'] = "Categorias"
        return context

class SucursalListView(ListView):
    model = Sucursal
    template_name = 'panel_admin/lista.html'
    context_object_name = 'objetos'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos'] = ['id', 'telefono', 'direccion', 'hora_inicio', 'hora_cierre']
        context['model_name'] = "Sucursales"
        return context

class EmpleadoListView(ListView):
    model = Empleado
    template_name = 'panel_admin/lista.html'
    context_object_name = 'objetos'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos'] = ['id', 'sucursal', 'area', 'nombre', 'apellido', 'cargo']
        context['model_name'] = "Empleados"
        return context

class ProductoVentaListView(ListView):
    model = ProductoVenta
    template_name = 'panel_admin/lista.html'
    context_object_name = 'objetos'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos'] = ['id', 'nombre', 'precio', 'descripcion', 'imagen']
        context['model_name'] = "ProductosVenta"
        return context

class ProductoPrimaListView(ListView):
    model = ProductoPrima
    template_name = 'panel_admin/lista.html'
    context_object_name = 'objetos'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos'] = ['id', 'categoria', 'nombre', 'precio', 'descripcion', 'imagen']
        context['model_name'] = "ProductosPrima"
        return context

class PaqueteListView(ListView):
    model = Paquete
    template_name = 'panel_admin/lista.html'
    context_object_name = 'objetos'
    paginate_by = 8 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos'] = ['id', 'proventa', 'proprima']
        context['model_name'] = "Paquetes"
        return context


class CrearObjetoView(CreateView):
    template_name = 'panel_admin/aniadir_editar.html'

    def get_model(self):
        model_name = self.kwargs['model_name']

        if model_name == 'areas':
            return Area, AreaForm
        elif model_name == 'categorias':
            return Categoria, CategoriaForm
        elif model_name == 'sucursales':
            return Sucursal, SucursalForm
        elif model_name == 'empleados':
            return Empleado, EmpleadoForm
        elif model_name == 'productosventa':
            return ProductoVenta, ProductoVentaForm
        elif model_name == 'productosprima':
            return ProductoPrima, ProductoPrimaForm
        elif model_name == 'paquetes':
            return Paquete, PaqueteForm

    def get_form_class(self):
        model, form_class = self.get_model()
        return form_class

    def get_success_url(self):
        model_name = self.kwargs["model_name"]
        if model_name == 'productosventa':
            return reverse_lazy('productos_venta_lista')
        elif model_name == 'productosprima':
            return reverse_lazy('productos_prima_lista')
        return reverse_lazy(f'{model_name}_lista') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.kwargs['model_name']
        return context

class EditarObjetoView(UpdateView):
    template_name = 'panel_admin/aniadir_editar.html'

    def get_model(self):
        model_name = self.kwargs['model_name']

        if model_name == 'productosprima':
            model_name = 'productos_prima'

        if model_name == 'areas':
            return Area, AreaForm
        elif model_name == 'categorias':
            return Categoria, CategoriaForm
        elif model_name == 'sucursales':
            return Sucursal, SucursalForm
        elif model_name == 'empleados':
            return Empleado, EmpleadoForm
        elif model_name == 'productosventa':
            return ProductoVenta, ProductoVentaForm
        elif model_name == 'productos_prima':
            return ProductoPrima, ProductoPrimaForm
        elif model_name == 'paquetes':
            return Paquete, PaqueteForm

    def get_form_class(self):
        model, form_class = self.get_model()
        return form_class

    def get_object(self):
        model, _ = self.get_model()
        return get_object_or_404(model, pk=self.kwargs['pk'])

    def get_success_url(self):
        model_name = self.kwargs["model_name"]
        if model_name == 'productosventa':
            return reverse_lazy('productos_venta_lista')
        elif model_name == 'productosprima':
            return reverse_lazy('productos_prima_lista')
        return reverse_lazy(f'{model_name}_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.kwargs['model_name']
        return context

class EliminarObjetoView(DeleteView):
    template_name = ''
    success_url = reverse_lazy('categorias_lista')

    def get_model(self):
        model_name = self.kwargs['model_name']

        if model_name == 'areas':
            return Area
        elif model_name == 'categorias':
            return Categoria
        elif model_name == 'sucursales':
            return Sucursal
        elif model_name == 'empleados':
            return Empleado
        elif model_name == 'productosventa':
            return ProductoVenta
        elif model_name == 'productosprima':
            return ProductoPrima
        elif model_name == 'paquetes':
            return Paquete

    def get_object(self):
        model = self.get_model()
        return get_object_or_404(model, pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, 'Registro eliminado exitosamente.')
        except IntegrityError:
            messages.error(request, 'No se puede eliminar el registro porque está relacionado.')
        return redirect(self.get_success_url())

    def get_success_url(self):
        model_name = self.kwargs["model_name"]
        if model_name == 'productosventa':
            return reverse_lazy('productos_venta_lista')
        elif model_name == 'productosprima':
            return reverse_lazy('productos_prima_lista')
        return reverse_lazy(f'{model_name}_lista')