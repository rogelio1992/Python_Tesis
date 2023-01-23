from atexit import register
from .models import *
from django.contrib import admin

# Register your models here.


class SynopAdmin(admin.ModelAdmin):
    list_display = ('id','estacion','fecha', 'hora') #Ahora la interfaz mostrará nombre, apellido y email de cada autor.
    search_fields = ('id','estacion','fecha', 'hora')

admin.site.register(Synop,SynopAdmin)
admin.site.register(Pronostico)
admin.site.register(Datos_adinociales)
admin.site.register(Provincia)
admin.site.register(Estacion)