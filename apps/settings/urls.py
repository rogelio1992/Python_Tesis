# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.settings.views import *

urlpatterns = [

    # The settings page

    path('ajustes/<int:pk>', General.as_view(), name='ajustes'),
    path('users/', UserListView.as_view(), name='users_list'),
    path('users/<int:pk>/details/', UserDetailView.as_view(), name='user_detail'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),



    path('contacto/list/', ContactoListView.as_view(), name='contacto_list'),
    #path('contacto/<int:pk>/details/', UserDetailView.as_view(), name='contacto_detail'),
    path('contacto/create/', ContactoCreateView.as_view(), name='contacto_create'),
    path('contacto/<int:pk>/update/', ContactoUpdateView.as_view(), name='contacto_update'),
    path('contacto/<int:pk>/delete/', ContactoDeleteView.as_view(), name='contacto_delete'),
    path('contactos/', Contactos.as_view() , name='contactos'),

   
]






 