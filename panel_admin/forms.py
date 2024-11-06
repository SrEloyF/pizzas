from django import forms
from api.models import *

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control col-md-6'

class AreaForm(BaseForm):
    class Meta:
        model = Area
        fields = ['nombre_area', 'descripcion']

class CategoriaForm(BaseForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']

class SucursalForm(BaseForm):
    class Meta:
        model = Sucursal
        fields = ['telefono', 'direccion', 'hora_inicio', 'hora_cierre']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control col-6'}),
            'hora_cierre': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control col-6'}),
        }

class EmpleadoForm(BaseForm):
    class Meta:
        model = Empleado
        fields = ['sucursal', 'area', 'nombre', 'apellido', 'cargo', 'estado']

class ProductoVentaForm(BaseForm):
    class Meta:
        model = ProductoVenta
        fields = ['repertorio','fecha_venta', 'estado']

class RepertorioForm(BaseForm):
    class Meta:
        model = Repertorio
        fields = ['titulo', 'descripcion', 'precio', 'fecha_inic', 'fecha_fin', 'imagen']
        widgets = {
            'fecha_inic': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
            }),
            'fecha_fin': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control-file col-md-6',
                'accept': '.png, .jpg, .jpeg'
            }),
        }


class ProductoPrimaForm(BaseForm):
    class Meta:
        model = ProductoPrima
        fields = ['categoria', 'nombre', 'precio', 'descripcion', 'stock']


class PaqueteForm(BaseForm):
    class Meta:
        model = Paquete
        fields = ['proventa', 'proprima']

class PedidoForm(BaseForm):
    class Meta:
        model = Pedido
        fields = ['sucursal', 'cliente', 'fecha_pedido', 'fecha_entrega', 'estado', 'nombre_ref', 'correo', 'direccion']
        widgets = {
            'fecha_pedido': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
            }),
            'fecha_entrega': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class DetallePedidoForm(BaseForm):
    class Meta:
        model = DetallePedido
        fields = ['pedido', 'proventa', 'cantidad', 'precio']

class PagoForm(BaseForm):
    class Meta:
        model = Pago
        fields = ['pedido', 'monto', 'metodo_pago', 'estado']

class HistorialForm(BaseForm):
    class Meta:
        model = Historial
        fields = ['empleado', 'pedido', 'detalle', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }

class ClienteForm(BaseForm):
    class Meta:
        model = Cliente
        fields = ['usuario', 'correo', 'telefono', 'contrasena']
        widgets = {
            'contrasena': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class UsuarioAdminForm(BaseForm):
    class Meta:
        model = UsuarioAdmin
        fields = ['usuario', 'rol', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

        

