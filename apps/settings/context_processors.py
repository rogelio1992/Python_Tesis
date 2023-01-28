from operator import imod
from django.shortcuts import render
from apps.settings.models import Settings
from apps.tiempo.models import Provincia

# Create your views here.


def extras(request):
    company_settings = Settings.objects.first()
    provincia = Provincia.objects.first()
    if company_settings == None:
        company_settings = Settings()
        company_settings.company_name = "Empresa"
        company_settings.miniature = "general/logo.png"
        company_settings.logo = "general/mini.png"
        company_settings.save()

    if provincia == None:
        # provincia = Provincia()
        # provincia.name = "Matanzas"
        # provincia.save()
        provincia = Provincia.objects.create(name="Matanzas")
    return {"company_settings": company_settings}
