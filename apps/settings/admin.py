from atexit import register
from xml.parsers.expat import model
from django.contrib import admin

from .models import CustomUser, Settings, Contacto

# Register your models here


admin.site.register(Settings)
admin.site.register(CustomUser)
admin.site.register(Contacto)
