# Generated by Django 5.1.2 on 2024-12-04 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_remove_pedido_correo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='repertorio',
            name='servidor',
            field=models.CharField(choices=[('android', 'Android'), ('web', 'Web')], default='web', max_length=50),
            preserve_default=False,
        ),
    ]
