
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import View
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin


from .models import *
from .forms import *


class General(LoginRequiredMixin, UpdateView):
    """
    Vista de la informacion del la compania
    """
    model = Settings
    fields = ('__all__')
    template_name = 'settings/general-settings.html'
    #success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = 'general-settings-company'
        return context


class UserBaseView(LoginRequiredMixin, View):
    """
    Clase de la cual heredan las demas vistas
    """
    model = CustomUser
    fields = ('username', 'first_name', 'last_name', 'email', 'permiss')
    success_url = reverse_lazy('users_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = 'general-settings-users'
        return context



class UserListView(UserBaseView, ListView):
    """
    Vista para listar usarios
    """
    template_name = 'settings/users/users_list.html'


class UserDetailView(UserBaseView, DetailView):
    """
    Vista para detallar usarios
    """
    template_name = 'settings/users/user_detail.html'


class UserCreateView(LoginRequiredMixin,CreateView):
    """
    Vista para crear usarios
    """
    model = CustomUser
    form_class = UserCreationForm
    template_name = 'settings/users/user_create.html'
    success_url = reverse_lazy('users_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = 'general-settings-users'
        return context


class UserUpdateView(LoginRequiredMixin ,UpdateView):
    """
    Vista para actualizar usarios
    """
    model = CustomUser
    fields = ('first_name', 'last_name', 'email', 'permiss')
    template_name = 'settings/users/user_update.html'
    success_url = reverse_lazy('users_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = 'general-settings-users'
        return context


class UserDeleteView(UserBaseView, DeleteView):
    """
    Vista para eliminar usarios
    """
    template_name = 'settings/users/user_delete.html'





"""
Al igual que la svistas de arriva se usan  para listar(ListView), crear(CreateView), actualizar(UpdateView),
eliminar(DeleteView) sea cual sea el modelo al que ahcen reperencia

LoginRequiredMixin -> Indica que esa vista requuire estar registrado para cceder a ella

"""
class ContactoListView(LoginRequiredMixin, ListView):
    model = Contacto
    template_name = 'settings/contacto/contacto_list.html'
    fields = ('__all__')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = 'general-settings-contacto'
        return context


class ContactoCreateView(LoginRequiredMixin,CreateView):
    model = Contacto
    fields = ('__all__')
    template_name = 'settings/contacto/contacto_create.html'
    success_url = reverse_lazy('contacto_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = 'general-settings-contacto'
        return context


class ContactoUpdateView(LoginRequiredMixin ,UpdateView):
    model = Contacto
    fields = ('__all__')
    template_name = 'settings/contacto/contacto_update.html'
    success_url = reverse_lazy('contacto_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = 'general-settings-contacto'
        return context


class ContactoDeleteView(LoginRequiredMixin, DeleteView):
    model = Contacto
    fields = ('__all__')
    template_name = 'settings/contacto/contacto_delete.html'
    success_url = reverse_lazy('contacto_list')

class Contactos(LoginRequiredMixin, ListView):
    model = Contacto
    fields = ('__all__')
    template_name = 'settings/contacto/contactos.html'
    success_url = reverse_lazy('contactos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = 'contactos'
        return context