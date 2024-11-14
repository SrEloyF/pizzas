# Generated by Django 5.1.2 on 2024-11-14 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='descripcion',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='descripcion',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='productoprima',
            name='descripcion',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='repertorio',
            name='descripcion',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterModelTable(
            name='area',
            table='areas',
        ),
        migrations.AlterModelTable(
            name='categoria',
            table='categorias',
        ),
        migrations.AlterModelTable(
            name='cliente',
            table='clientes',
        ),
        migrations.AlterModelTable(
            name='detallepedido',
            table='detalles_pedido',
        ),
        migrations.AlterModelTable(
            name='empleado',
            table='empleados',
        ),
        migrations.AlterModelTable(
            name='historial',
            table='historial',
        ),
        migrations.AlterModelTable(
            name='pago',
            table='pagos',
        ),
        migrations.AlterModelTable(
            name='paquete',
            table='paquetes',
        ),
        migrations.AlterModelTable(
            name='pedido',
            table='pedidos',
        ),
        migrations.AlterModelTable(
            name='productoprima',
            table='productos_prima',
        ),
        migrations.AlterModelTable(
            name='productoventa',
            table='productos_venta',
        ),
        migrations.AlterModelTable(
            name='repertorio',
            table='repertorios',
        ),
        migrations.AlterModelTable(
            name='sucursal',
            table='sucursales',
        ),
    ]
