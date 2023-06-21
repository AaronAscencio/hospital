from typing import Any
from django.forms.models import model_to_dict
from django.db import transaction
from django.http import HttpRequest, HttpResponse,HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
import json
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,FormView,View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from pkg_resources import safe_extra
from core.user.mixins import ValidatePermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from .models import *
from .forms import *
from django.contrib import messages
from datetime import date
from core.appointment.models import Appointment
# Create your views here.

class OfficeListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Office
    template_name = 'office/list.html'
    permission_required = 'office.view_office'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for office in Office.objects.all():
                    data.append(office.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Consultorios'
        context['create_url'] = reverse_lazy('office:office_create')
        context['list_url'] = reverse_lazy('office:office_list')
        context['entity'] = 'Consultorios'
        return context
    
class OfficeCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = Office
    form_class = OfficeForm
    template_name = 'office/create.html'
    permission_required = 'office.add_office'
    success_url = reverse_lazy('office:office_list')
    #permission_required = 'user.add_user'
    #url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Consultorio'
        context['entity'] = 'Consultorio'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class OfficeUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Office
    form_class = OfficeForm
    template_name = 'office/create.html'
    success_url = reverse_lazy('office:office_list')
    permission_required = 'office.change_office'
    #url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Consultorio'
        context['entity'] = 'Consultorios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class OfficeDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    
    model = Office
    template_name = 'office/delete.html'
    success_url = reverse_lazy('office:office_list')
    permission_required = 'office.delete_office'
    #url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        current_date = date.today()
        doctor_appointments = Appointment.objects.filter(office_id=self.object.pk,date__gte= current_date)
        if doctor_appointments.exists():
            messages.error(request,'No puedes eliminar este consultorio, ya que cuenta con consultas asignadas')
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Consultorio'
        context['entity'] = 'Consultorios'
        context['list_url'] = self.success_url
        return context