# Generated by Django 5.1.2 on 2024-12-06 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_rename_nombre_ref_pedido_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='productoventa',
            name='codigo',
            field=models.CharField(default='', max_length=15),
            preserve_default=False,
        ),
    ]
