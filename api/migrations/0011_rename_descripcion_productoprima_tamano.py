# Generated by Django 5.1.2 on 2024-12-03 00:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_detallerepertorio_producto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productoprima',
            old_name='descripcion',
            new_name='tamano',
        ),
    ]