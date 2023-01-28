# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.tiempo.views import *
from apps.tiempo.render_to_pdf import *
from apps.tiempo.export_img import pronosticoImage

urlpatterns = [
    path("", LastPronostico.as_view(), name="home"),
    path("resumen/", Resumen.as_view(), name="resumen_tiempo"),
    path("synop/utiles/", Utiles.as_view(), name="utiles"),
    path(
        "synop/utiles/reporte_diario/", ReporteDiario.as_view(), name="reporte_diario"
    ),
    # path('synop/<int:pk>/pdf_view/', ViewPDF.as_view(), name= 'pdf_view'),
    path("synop/<int:pk>/pdf_dowload/", DownloadPDF.as_view(), name="pdf_dowload"),
    # path('synop/utiles/pdf_view/', GeneralViewPDF.as_view(), name= 'pdf_view_general'),
    # e path('synop/utiles/pdf_dowload/', GeneralDownloadPDF.as_view(), name= 'pdf_dowload_general'),
    path("synop/", Parser.as_view(), name="suynop_parser"),
    path("synop/list/", SynopListView.as_view(), name="synop_list"),
    path("synop/<int:pk>/update/", SynopUpdateView.as_view(), name="synop_update"),
    path("synop/<int:pk>/delete/", SynopDeleteView.as_view(), name="synop_delete"),
    path("synop/<int:pk>/details/", SynopDetailView.as_view(), name="synop_detail"),
    path(
        "synop/<int:id>/datos_adinociales/",
        DatosAdinocialesListView.as_view(),
        name="datos_adinociales_list",
    ),
    path(
        "synop/<int:id>/datos_adinociales/<int:pk>/update/",
        DatosAdinocialesUpdateView.as_view(),
        name="datos_adinociales_update",
    ),
    path(
        "synop/<int:id>/datos_adinociales/<int:pk>/delete/",
        SynopDeleteView.as_view(),
        name="datos_adinociales_delete",
    ),
    path(
        "synop/<int:pk>/details/",
        SynopDetailView.as_view(),
        name="datos_adinociales_detail",
    ),
    path("pronostico/list/", PronosticoListView.as_view(), name="pronostico_list"),
    path(
        "pronostico/create/", PronosticoCreateView.as_view(), name="pronostico_create"
    ),
    path(
        "pronostico/<int:pk>/update/",
        PronosticoUpdateView.as_view(),
        name="pronostico_update",
    ),
    path(
        "pronostico/<int:pk>/delete/",
        PronosticoDeleteView.as_view(),
        name="pronostico_delete",
    ),
    path(
        "pronostico/<int:pk>/details/",
        PronosticoDetailView.as_view(),
        name="pronostico_detail",
    ),
    path("pronostico/<int:pk>/img/", pronosticoImage, name="pronostico_img"),
    # path('synops/create/', synopCreateView.as_view(), name='synop_create'),
    # path('ajustes/<int:pk>', General.as_view(), name='ajustes'),
    path("provincia/list/", ProvinciaListView.as_view(), name="provincia_list"),
    path("provincia/create/", ProvinciaCreateView.as_view(), name="provincia_create"),
    path(
        "provincia/<int:pk>/update/",
        ProvinciaUpdateView.as_view(),
        name="provincia_update",
    ),
    path(
        "provincia/<int:pk>/delete/",
        ProvinciaDeleteView.as_view(),
        name="provincia_delete",
    ),
    path("estacion/list/", EstacionListView.as_view(), name="estacion_list"),
    path("estacion/create/", EstacionCreateView.as_view(), name="estacion_create"),
    path(
        "estacion/<int:pk>/update/",
        EstacionUpdateView.as_view(),
        name="estacion_update",
    ),
    path(
        "estacion/<int:pk>/delete/",
        EstacionDeleteView.as_view(),
        name="estacion_delete",
    ),
]
