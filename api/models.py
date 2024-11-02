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

    usuario = models.CharField(max_length=50, unique=True)
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
    nombre_area = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre_area

class Categoria(models.Model):
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=70)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    usuario = models.CharField(max_length=45)
    correo = models.EmailField(max_length=50)
    telefono = models.IntegerField()
    contrasena = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Sucursal(models.Model):
    telefono = models.IntegerField()
    direccion = models.CharField(max_length=45)
    hora_inicio = models.TimeField()
    hora_cierre = models.TimeField()

    def __str__(self):
        return self.direccion

class Pedido(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateField()
    estado = models.CharField(max_length=45)
    nombre_ref = models.CharField(max_length=45)
    correo = models.CharField(max_length=85)
    direccion = models.CharField(max_length=85)

    def __str__(self):
        return f"Pedido {self.pk} - {self.estado}"

class Pedido(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    #pago = models.ForeignKey(Pago, on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateField()
    estado = models.CharField(max_length=45)
    nombre_ref = models.CharField(max_length=45)
    correo = models.CharField(max_length=85)
    direccion = models.CharField(max_length=85)

    def __str__(self):
        return f"Pedido {self.pk} - {self.estado}"
    
class Pago(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=45)
    estado = models.CharField(max_length=45)

    def __str__(self):
        return f"Pago {self.pk} - {self.estado}"

class ProductoVenta(models.Model):
    nombre = models.CharField(max_length=70)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=45)
    imagen = models.ImageField(upload_to='productos_venta/', null=True, blank=True)

    def __str__(self):
        return self.nombre

class ProductoPrima(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=45)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='productos_prima/', null=True, blank=True)

    def __str__(self):
        return self.nombre

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
    proventa = models.ForeignKey(ProductoVenta, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle {self.pk} - Pedido {self.pedido.pk}"

class Paquete(models.Model):
    proventa = models.ForeignKey(ProductoVenta, on_delete=models.PROTECT)
    proprima = models.ForeignKey(ProductoPrima, on_delete=models.PROTECT)

    def __str__(self):
        return f"Paquete {self.pk}"

class Empleado(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('no_disponible', 'No Disponible'),
    ]

    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    cargo = models.CharField(max_length=45)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='disponible')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Historial(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT)
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
    detalle = models.CharField(max_length=45)
    fecha = models.DateField()

    def __str__(self):
        return f"Historial {self.pk} - Pedido {self.pedido.pk}"
