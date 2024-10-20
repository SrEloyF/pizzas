from django.db import models

class Area(models.Model):
    id_area = models.CharField(max_length=45, primary_key=True)
    nombre_area = models.CharField(max_length=45, null=True, blank=True)
    descripcion = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return self.nombre_area

class Categoria(models.Model):
    id_categoria = models.CharField(max_length=45, primary_key=True)
    nombre = models.CharField(max_length=45, null=True, blank=True)
    descripcion = models.CharField(max_length=70, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45, null=True, blank=True)
    apellido = models.CharField(max_length=45, null=True, blank=True)
    correo = models.EmailField(max_length=50, null=True, blank=True)
    telefono = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Sucursal(models.Model):
    id_sucursal = models.AutoField(primary_key=True)
    telefono = models.IntegerField(null=True, blank=True)
    direccion = models.CharField(max_length=45, null=True, blank=True)
    hora_inicio = models.CharField(max_length=45, null=True, blank=True)
    hora_cierre = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return self.direccion

class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    metodo_pago = models.CharField(max_length=45, null=True, blank=True)
    estado = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return f"Pago {self.id_pago} - {self.estado}"

class Pedido(models.Model):
    id_pedido = models.CharField(max_length=100, primary_key=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True)
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=45, null=True, blank=True)
    estado = models.CharField(max_length=45, null=True, blank=True)
    nombre_ref = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return f"Pedido {self.id_pedido} - {self.estado}"

class ProductoVenta(models.Model):
    id_proventa = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=70, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    descripcion = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return self.nombre

class ProductoPrima(models.Model):
    id_proprima = models.AutoField(primary_key=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    nombre = models.CharField(max_length=45, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    descripcion = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nombre

class DetallePedido(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    proventa = models.ForeignKey(ProductoVenta, on_delete=models.SET_NULL, null=True)
    cantidad = models.IntegerField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Detalle {self.id_detalle} - Pedido {self.pedido.id_pedido}"

class Paquete(models.Model):
    id_paquete = models.AutoField(primary_key=True)
    proventa = models.ForeignKey(ProductoVenta, on_delete=models.CASCADE)
    proprima = models.ForeignKey(ProductoPrima, on_delete=models.CASCADE)

    def __str__(self):
        return f"Paquete {self.id_paquete}"

class Empleado(models.Model):
    id_empleado = models.CharField(max_length=45, primary_key=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    nombre = models.CharField(max_length=45, null=True, blank=True)
    apellido = models.CharField(max_length=45, null=True, blank=True)
    cargo = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Historial(models.Model):
    id_historial = models.CharField(max_length=45, primary_key=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True)
    estado = models.CharField(max_length=45, null=True, blank=True)
    fecha = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Historial {self.id_historial} - Pedido {self.pedido.id_pedido}"
