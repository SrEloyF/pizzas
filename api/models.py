from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UsuarioAdminManager(BaseUserManager):
    def create_user(self, usuario, password=None, **extra_fields):
        if not usuario:
            raise ValueError('El usuario debe tener un nombre de usuario')
        extra_fields.setdefault('is_active', True)
        user = self.model(usuario=usuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuario debe tener is_superuser=True.')

        return self.create_user(usuario, password, **extra_fields)

    def get_by_natural_key(self, usuario):
        return self.get(usuario=usuario)

class UsuarioAdmin(AbstractBaseUser, PermissionsMixin):
    ROL_CHOICES = [
        ('general', 'General'),
        ('otro', 'Otro'),
    ]

    usuario = models.CharField(max_length=1024, unique=True)
    rol = models.CharField(max_length=10, choices=ROL_CHOICES)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = []

    objects = UsuarioAdminManager()

    def __str__(self):
        return self.usuario
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

class Area(models.Model):
    id_area = models.AutoField(primary_key=True)
    nombre_area = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=300)

    def __str__(self):
        return  self.nombre_area
    
    class Meta:
        db_table = 'areas'

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=300)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'categorias'

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=45, unique=True)
    correo = models.EmailField(max_length=50, unique=True)
    telefono = models.IntegerField()
    contrasena = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.usuario} - {self.correo}"
    
    class Meta:
        db_table = 'clientes'

class Sucursal(models.Model):
    id_sucursal = models.AutoField(primary_key=True)
    telefono = models.IntegerField()
    direccion = models.CharField(max_length=45)
    hora_inicio = models.TimeField()
    hora_cierre = models.TimeField()

    def __str__(self):
        return self.direccion
    
    class Meta:
        db_table = 'sucursales'

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    id_sucursal = models.ForeignKey(Sucursal, db_column='id_sucursal',on_delete=models.PROTECT)
    id_cliente = models.ForeignKey(Cliente, db_column='id_cliente',on_delete=models.PROTECT)
    fecha_pedido = models.DateTimeField()
    fecha_entrega = models.DateTimeField()
    estado = models.CharField(max_length=45)
    nombre_ref = models.CharField(max_length=45)
    correo = models.CharField(max_length=85)
    direccion = models.CharField(max_length=85)

    class Meta:
        db_table = 'pedidos'
        unique_together = (('id_pedido', 'id_sucursal'),)

    def __str__(self):
        return f"Pedido {self.id_pedido} - {self.estado}"
    
class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedido, db_column='id_pedido', on_delete=models.PROTECT)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=45)
    estado = models.CharField(max_length=45)

    class Meta:
        db_table = 'pagos'
        unique_together = (('id_pago', 'id_pedido'),)

    def __str__(self):
        return f"Pago {self.id_pago} - {self.estado}"

class Repertorio(models.Model):
    id_repertorio = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=300)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inic = models.DateField()
    fecha_fin = models.DateField()
    tipo_repertorio = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='repertorio/', null=True, blank=True)

    class Meta:
        db_table = 'repertorios'

    def __str__(self):
        return f"{self.id_repertorio} - {self.titulo}"
    
class DetalleRepertorio(models.Model):
    id_detalle_repertorio = models.AutoField(primary_key=True)
    id_repertorio = models.ForeignKey(Repertorio, db_column='id_repertorio', on_delete=models.PROTECT)
    producto = models.CharField(max_length=100)
    unidades = models.PositiveIntegerField()
    detalle = models.CharField(max_length=200)

    class Meta:
        db_table = 'detalles_repertorio'
    
    def __str__(self):
        return f"{self.id_detalle_repertorio} - {self.producto}"

class ProductoVenta(models.Model):
    id_proventa = models.AutoField(primary_key=True)
    id_repertorio = models.ForeignKey(Repertorio, db_column='id_repertorio', on_delete= models.PROTECT)
    fecha_venta = models.DateField()
    estado = models.CharField(max_length=45)

    class Meta:
        db_table = 'productos_venta'

    def __str__(self):
        return f"Prod Venta {self.id_proventa} - {self.fecha_venta} - {self.estado}"

class ProductoPrima(models.Model):
    id_proprima = models.AutoField(primary_key=True)
    id_categoria = models.ForeignKey(Categoria, db_column='id_categoria',on_delete=models.PROTECT)
    nombre = models.CharField(max_length=45)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=300)
    stock = models.PositiveIntegerField()

    class Meta:
        db_table = 'productos_prima'
        unique_together = (('id_proprima', 'id_categoria'),)

    def __str__(self):
        return self.nombre

class DetallePedido(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedido, db_column='id_pedido',on_delete=models.PROTECT)
    id_proventa = models.ForeignKey(ProductoVenta, db_column='id_proventa', on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalles_pedido'
        unique_together = (('id_detalle', 'id_pedido', 'id_proventa'),)

    def __str__(self):
        return f"Detalle {self.id_detalle} - Pedido {self.id_pedido}"

class Paquete(models.Model):
    id_paquete = models.AutoField(primary_key=True)
    id_proventa = models.ForeignKey(ProductoVenta, db_column='id_proventa',on_delete=models.PROTECT)
    id_proprima = models.ForeignKey(ProductoPrima, db_column='id_proprima', on_delete=models.PROTECT)

    class Meta:
        db_table = 'paquetes'
        unique_together = (('id_paquete', 'id_proventa', 'id_proprima'),)

    def __str__(self):
        return f"Paquete {self.id_paquete}"

class Empleado(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('no_disponible', 'No Disponible'),
    ]
    id_empleado = models.AutoField(primary_key=True)
    id_sucursal = models.ForeignKey(Sucursal, db_column='id_sucursal',on_delete=models.PROTECT)
    id_area = models.ForeignKey(Area, db_column='id_area',on_delete=models.PROTECT)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    cargo = models.CharField(max_length=45)
    estado = models.CharField(max_length=25, choices=ESTADO_CHOICES, default='disponible')

    class Meta:
        db_table = 'empleados'
        unique_together = (('id_empleado', 'id_sucursal', 'id_area'),)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Historial(models.Model):
    id_historial = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(Empleado, db_column='id_empleado',on_delete=models.PROTECT)
    id_pedido = models.ForeignKey(Pedido, db_column='id_pedido', on_delete=models.PROTECT)
    detalle = models.CharField(max_length=45)
    fecha = models.DateField()

    class Meta:
        db_table = 'historial'
        unique_together = (('id_historial', 'id_empleado', 'id_pedido'),)

    def __str__(self):
        return f"Historial {self.id_historial} - Pedido {self.id_pedido}"