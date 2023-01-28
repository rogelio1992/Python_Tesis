# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from multiprocessing import context
from urllib import response
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.template import RequestContext, Template
from django.shortcuts import render
from apps.settings.models import Settings


"""
Estas vistas viene con la plantilla no estan siendo usadas en este momento, se mantienes pra hacer prubas solamente

"""


@login_required(login_url="/login/")
def index(request):
    context = {"segment": "dashboard"}

    html_template = loader.get_template("home/dashboard.html")

    return HttpResponse(html_template.render(context, request))


@login_required(login_url="accounts/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split("/")[-1]

        if load_template == "admin":
            return HttpResponseRedirect(reverse("admin:index"))

        context["segment"] = load_template

        html_template = loader.get_template("home/" + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template("home/page-404.html")
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template("home/page-500.html")
        return HttpResponse(html_template.render(context, request))
