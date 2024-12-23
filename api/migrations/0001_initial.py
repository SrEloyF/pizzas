# Generated by Django 5.1.2 on 2024-11-18 14:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id_area', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_area', models.CharField(max_length=45)),
                ('descripcion', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'areas',
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id_categoria', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=45)),
                ('descripcion', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'categorias',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id_cliente', models.AutoField(primary_key=True, serialize=False)),
                ('usuario', models.CharField(max_length=45)),
                ('correo', models.EmailField(max_length=50, unique=True)),
                ('telefono', models.IntegerField()),
                ('contrasena', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'clientes',
            },
        ),
        migrations.CreateModel(
            name='Repertorio',
            fields=[
                ('id_repertorio', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=60)),
                ('descripcion', models.CharField(max_length=300)),
                ('precio', models.DecimalField(decimal_places=5, max_digits=10)),
                ('fecha_inic', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='repertorio/')),
            ],
            options={
                'db_table': 'repertorios',
            },
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id_sucursal', models.AutoField(primary_key=True, serialize=False)),
                ('telefono', models.IntegerField()),
                ('direccion', models.CharField(max_length=45)),
                ('hora_inicio', models.TimeField()),
                ('hora_cierre', models.TimeField()),
            ],
            options={
                'db_table': 'sucursales',
            },
        ),
        migrations.CreateModel(
            name='UsuarioAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('usuario', models.CharField(max_length=1024, unique=True)),
                ('rol', models.CharField(choices=[('general', 'General'), ('otro', 'Otro')], max_length=10)),
                ('is_staff', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id_empleado', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=45)),
                ('apellido', models.CharField(max_length=45)),
                ('cargo', models.CharField(max_length=45)),
                ('estado', models.CharField(choices=[('disponible', 'Disponible'), ('no_disponible', 'No Disponible')], default='disponible', max_length=25)),
                ('id_area', models.ForeignKey(db_column='id_area', on_delete=django.db.models.deletion.PROTECT, to='api.area')),
                ('id_sucursal', models.ForeignKey(db_column='id_sucursal', on_delete=django.db.models.deletion.PROTECT, to='api.sucursal')),
            ],
            options={
                'db_table': 'empleados',
                'unique_together': {('id_empleado', 'id_sucursal', 'id_area')},
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id_pedido', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_pedido', models.DateTimeField()),
                ('fecha_entrega', models.DateTimeField()),
                ('estado', models.CharField(max_length=45)),
                ('nombre_ref', models.CharField(max_length=45)),
                ('correo', models.CharField(max_length=85)),
                ('direccion', models.CharField(max_length=85)),
                ('id_cliente', models.ForeignKey(db_column='id_cliente', on_delete=django.db.models.deletion.PROTECT, to='api.cliente')),
                ('id_sucursal', models.ForeignKey(db_column='id_sucursal', on_delete=django.db.models.deletion.PROTECT, to='api.sucursal')),
            ],
            options={
                'db_table': 'pedidos',
                'unique_together': {('id_pedido', 'id_sucursal')},
            },
        ),
        migrations.CreateModel(
            name='ProductoPrima',
            fields=[
                ('id_proprima', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=45)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('descripcion', models.CharField(max_length=300)),
                ('stock', models.PositiveIntegerField()),
                ('id_categoria', models.ForeignKey(db_column='id_categoria', on_delete=django.db.models.deletion.PROTECT, to='api.categoria')),
            ],
            options={
                'db_table': 'productos_prima',
                'unique_together': {('id_proprima', 'id_categoria')},
            },
        ),
        migrations.CreateModel(
            name='ProductoVenta',
            fields=[
                ('id_proventa', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_venta', models.DateField()),
                ('estado', models.CharField(max_length=45)),
                ('id_repertorio', models.ForeignKey(db_column='id_repertorio', on_delete=django.db.models.deletion.PROTECT, to='api.repertorio')),
            ],
            options={
                'db_table': 'productos_venta',
            },
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id_pago', models.AutoField(primary_key=True, serialize=False)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('metodo_pago', models.CharField(max_length=45)),
                ('estado', models.CharField(max_length=45)),
                ('id_pedido', models.ForeignKey(db_column='id_pedido', on_delete=django.db.models.deletion.PROTECT, to='api.pedido')),
            ],
            options={
                'db_table': 'pagos',
                'unique_together': {('id_pago', 'id_pedido')},
            },
        ),
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id_historial', models.AutoField(primary_key=True, serialize=False)),
                ('detalle', models.CharField(max_length=45)),
                ('fecha', models.DateField()),
                ('id_empleado', models.ForeignKey(db_column='id_empleado', on_delete=django.db.models.deletion.PROTECT, to='api.empleado')),
                ('id_pedido', models.ForeignKey(db_column='id_pedido', on_delete=django.db.models.deletion.PROTECT, to='api.pedido')),
            ],
            options={
                'db_table': 'historial',
                'unique_together': {('id_historial', 'id_empleado', 'id_pedido')},
            },
        ),
        migrations.CreateModel(
            name='Paquete',
            fields=[
                ('id_paquete', models.AutoField(primary_key=True, serialize=False)),
                ('id_proprima', models.ForeignKey(db_column='id_proprima', on_delete=django.db.models.deletion.PROTECT, to='api.productoprima')),
                ('id_proventa', models.ForeignKey(db_column='id_proventa', on_delete=django.db.models.deletion.PROTECT, to='api.productoventa')),
            ],
            options={
                'db_table': 'paquetes',
                'unique_together': {('id_paquete', 'id_proventa', 'id_proprima')},
            },
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id_detalle', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_pedido', models.ForeignKey(db_column='id_pedido', on_delete=django.db.models.deletion.PROTECT, to='api.pedido')),
                ('id_proventa', models.ForeignKey(db_column='id_proventa', on_delete=django.db.models.deletion.PROTECT, to='api.productoventa')),
            ],
            options={
                'db_table': 'detalles_pedido',
                'unique_together': {('id_detalle', 'id_pedido', 'id_proventa')},
            },
        ),
    ]