# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("accounts/login/", login_view, name="login"),
    path("accounts/register/", register_user, name="register"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path("accounts/profile/<int:pk>", Profile.as_view(), name="profile"),
    path(
        "accounts/password-change/",
        ChangePasswordView.as_view(),
        name="password_change",
    ),
]
