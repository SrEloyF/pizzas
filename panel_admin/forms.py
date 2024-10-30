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
        fields = ['nombre', 'precio', 'descripcion', 'imagen']
        widgets = {
            'imagen': forms.FileInput(attrs={
                'class': 'form-control-file col-md-6',
                'accept': '.png, .jpg, .jpeg'
            }),
        }

class ProductoPrimaForm(BaseForm):
    class Meta:
        model = ProductoPrima
        fields = ['categoria', 'nombre', 'precio', 'descripcion', 'imagen']
        widgets = {
            'imagen': forms.FileInput(attrs={
                'class': 'form-control-file col-md-6',
                'accept': '.png, .jpg, .jpeg'
            }),
        }

class PaqueteForm(BaseForm):
    class Meta:
        model = Paquete
        fields = ['proventa', 'proprima']

class UsuarioAdminForm(BaseForm):
    class Meta:
        model = UsuarioAdmin
        fields = ['usuario', 'rol', 'password']

"""
class SuperUsuarioForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    class Meta:
        model = SuperUsuario
        fields = ['usuario', 'contrasena', 'rol']

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data['contrasena'])
        if commit:
            usuario.save()
        return usuario
"""