# Generated by Django 5.1.2 on 2024-10-22 22:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_area', models.CharField(max_length=45)),
                ('descripcion', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('descripcion', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('apellido', models.CharField(max_length=45)),
                ('correo', models.EmailField(max_length=50)),
                ('telefono', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('metodo_pago', models.CharField(max_length=45)),
                ('estado', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='ProductoVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=70)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('descripcion', models.CharField(max_length=45)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='productos_venta/')),
            ],
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefono', models.IntegerField()),
                ('direccion', models.CharField(max_length=45)),
                ('hora_inicio', models.TimeField()),
                ('hora_cierre', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('apellido', models.CharField(max_length=45)),
                ('cargo', models.CharField(max_length=45)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.area')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.sucursal')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pedido', models.DateTimeField(auto_now_add=True)),
                ('fecha_entrega', models.DateField()),
                ('direccion', models.CharField(max_length=45)),
                ('estado', models.CharField(max_length=45)),
                ('nombre_ref', models.CharField(max_length=45)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.cliente')),
                ('pago', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.pago')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.sucursal')),
            ],
        ),
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=45)),
                ('fecha', models.DateField()),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.empleado')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.pedido')),
            ],
        ),
        migrations.CreateModel(
            name='ProductoPrima',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('descripcion', models.CharField(max_length=100)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='productos_prima/')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Paquete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proprima', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.productoprima')),
                ('proventa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.productoventa')),
            ],
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.pedido')),
                ('proventa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.productoventa')),
            ],
        ),
    ]
