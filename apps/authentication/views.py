 # -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from django.views.generic import View, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

from apps.settings.models import Settings,CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin

class Profile(LoginRequiredMixin,UpdateView):
    """
        Esta vista es en la que se determina la informacion que se envia al template del Perfil
    """
    model = CustomUser
    fields = ['first_name','last_name','email','avatar',]
    template_name = 'accounts/profile.html'
    

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.get_object().id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = 'profile'
        return context


class ChangePasswordView(LoginRequiredMixin,SuccessMessageMixin, PasswordChangeView):
    """
    Esta vista es con la que se cambia la contraseña y el mensaje  que se muestra en caso de hacerlo
    """
    template_name = 'accounts/change_password.html'
    success_message = "Contraseña cambiada satisfactoriamente"
    
    def get_success_url(self):
        
        return reverse('profile', kwargs={'pk':self.request.user.id})





def login_view(request):
    """
    Viata del Login
    """
    form = LoginForm(request.POST or None)
    msg = None
  
    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Credenciales invalidas'
        else:
            msg = 'Error validando el formulario'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    """
    Viata para registrarse un usuario por si mismo en este momento no esta en uso
    """
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
