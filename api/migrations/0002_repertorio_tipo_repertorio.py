# Generated by Django 5.1.2 on 2024-11-20 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='repertorio',
            name='tipo_repertorio',
            field=models.CharField(default='-', max_length=100),
            preserve_default=False,
        ),
    ]