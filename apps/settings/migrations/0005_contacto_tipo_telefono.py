# Generated by Django 3.2.11 on 2022-12-17 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0004_auto_20221216_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacto',
            name='tipo_telefono',
            field=models.CharField(choices=[('Movil', 'movil'), ('Fijo', 'Fijo')], default='Movil', max_length=250, verbose_name='Cargo'),
        ),
    ]
