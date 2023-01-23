import os
from secrets import choice

from django.urls import reverse
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import pre_save


permis = (
    ("Usuario","Usuario"),
    ("Especialista","Especialista"),
    ("Administrador","Administrador"),
  
)

class CustomUser(AbstractUser):
    avatar = models.ImageField("Foto de perfil", upload_to='usuarios/', height_field=None, width_field=None, max_length=None,null=True, blank=True)
    permiss = models.CharField("Permisos", choices=permis, max_length=250)
    
  
"""@receiver(models.signals.post_delete, sender=CustomUser)
def auto_delete_file_on_delete(sender, instance, **kwargs):
   
    Deletes file from filesystem
    when corresponding `CustomUser` object is deleted.
   
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)


@receiver(pre_save, sender=CustomUser)
def delete_old_file(sender, instance, **kwargs):
    # on creation, signal callback won't be triggered 
    if instance._state.adding and not instance.pk:
        return False
    
    try:
        old_file = sender.objects.get(pk=instance.pk).avatar
    except sender.DoesNotExist:
        return False
    
    # comparing the new file with the old one
    file = instance.avatar
    if not old_file == file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
"""



class Settings(models.Model):
    id = models.AutoField(primary_key=True)
    miniature = models.ImageField("Miniatura", upload_to='general/', height_field=None, width_field=None, max_length=None,null=True, blank=True )
    logo = models.ImageField("Logo", upload_to='general/', height_field=None, width_field=None, max_length=None,null=True, blank=True)
    company_name = models.CharField("Nombre de la Compañía", max_length=50)
    company_email = models.EmailField("Correo", max_length=254, blank=True, null=True)
    company_phone = PhoneNumberField("Teléfono",blank=True, null=True)
   
    class Meta:
        verbose_name = "Ajuste"
        verbose_name_plural = "Ajustes"

    def __str__(self):
        return "Ajustes generales"
    
    def get_absolute_url(self): # new
        return reverse('ajustes', args=[str(self.id)])


tipo_telefono = (('Móvil','Móvil'),('Fijo','Fijo'))

class Contacto(models.Model):

    nombre = models.CharField("Nombre", max_length=250)
    telefono = models.CharField("Teléfono", max_length=250, blank=True, null=True)
    tipo_telefono = models.CharField("Tipo de teléfono", max_length=250, choices=tipo_telefono, default='Móvil')
    correo = models.EmailField("Correo", max_length=250, blank=True, null=True, unique=True)

    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"

    def __str__(self):
        return self.nombre





"""
@receiver(models.signals.post_delete, sender=Settings)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.miniature:
        if os.path.isfile(instance.miniature.path):
            os.remove(instance.miniature.path)
    if instance.logo:
        if os.path.isfile(instance.logo.path):
            os.remove(instance.logo.path)

@receiver(models.signals.pre_save, sender=Settings)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Settings.objects.get(pk=instance.pk).miniature
    except Settings.DoesNotExist:
        return False

    new_file = instance.miniature

    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


    try:
        old_file = Settings.objects.get(pk=instance.pk).logo
    except Settings.DoesNotExist:
        return False

    new_file = instance.logo
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
"""