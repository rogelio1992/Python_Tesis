# Generated by Django 3.2.11 on 2022-12-10 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='permiss',
            field=models.CharField(choices=[('Usuario', 'Usuario'), ('Especialista', 'Especialista'), ('Administrador', 'Administrador')], max_length=250, verbose_name='Permisos'),
        ),
    ]
