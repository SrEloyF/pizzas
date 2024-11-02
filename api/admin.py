from django.contrib import admin
from .models import (
    UsuarioAdmin,
    Area,
    Categoria,
    Cliente,
    Sucursal,
    Pago,
    Pedido,
    ProductoVenta,
    ProductoPrima,
    DetallePedido,
    Paquete,
    Empleado,
    Historial
)

@admin.register(UsuarioAdmin)
class UsuarioAdminAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'is_staff', 'is_active')
    search_fields = ('usuario',)

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('nombre_area', 'descripcion')
    search_fields = ('nombre_area',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'correo', 'telefono')
    search_fields = ('usuario', 'correo')

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('direccion', 'telefono', 'hora_inicio', 'hora_cierre')
    search_fields = ('direccion',)

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('monto', 'metodo_pago', 'estado')
    search_fields = ('metodo_pago', 'estado')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'sucursal', 'fecha_pedido', 'estado')
    search_fields = ('nombre_ref', 'correo', 'direccion')

@admin.register(ProductoVenta)
class ProductoVentaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'descripcion')
    search_fields = ('nombre',)

@admin.register(ProductoPrima)
class ProductoPrimaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'descripcion')
    search_fields = ('nombre',)

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'proventa', 'cantidad', 'precio')
    search_fields = ('pedido__pk',)

@admin.register(Paquete)
class PaqueteAdmin(admin.ModelAdmin):
    list_display = ('proventa', 'proprima')
    search_fields = ('proventa__nombre',)

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'cargo', 'estado')
    search_fields = ('nombre', 'apellido')

@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'pedido', 'detalle', 'fecha')
    search_fields = ('detalle',)

