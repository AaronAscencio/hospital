from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from core.user.mixins import ValidatePermissionRequiredMixin
from django.contrib.auth.models import Group
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, FormView
from .models import Appointment
from .forms import AppointmentForm,AppointmentByDoctorForm,AppointmentByPatientForm
from django.contrib import messages
from datetime import datetime, timedelta

class AppointmentListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Appointment
    template_name = 'appointment/list.html'
    permission_required = 'appointment.view_appointment'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Appointment.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Citas'
        context['create_url'] = reverse_lazy('appointment:appointment_create')
        context['list_url'] = reverse_lazy('appointment:appointment_list')
        context['entity'] = 'Citas'
        return context
    
class AppointmentCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment/create.html'
    permission_required = 'appointment.add_appointment'
    success_url = reverse_lazy('appointment:appointment_list')
    #permission_required = 'user.add_user'
    url_redirect = success_url

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
        context['title'] = 'Creación de una Cita'
        context['entity'] = 'Citas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class AppointmentUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment/create.html'
    success_url = reverse_lazy('appointment:appointment_list')
    permission_required = 'appointment.change_appointment'
    url_redirect = success_url

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
        context['title'] = 'Edición de una Cita'
        context['entity'] = 'Citas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class AppointmentDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    
    model = Appointment
    template_name = 'appointment/delete.html'
    success_url = reverse_lazy('appointment:appointment_list')
    permission_required = 'appointment.delete_appointment'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        current_date = datetime.now().date()
        if self.object.date - current_date < timedelta(days=1):
            messages.error(request,'No puedes cancelar/eliminar la cita en un periodo menor a las 24 horas de esta misma')
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
        context['title'] = 'Eliminación de una Cita'
        context['entity'] = 'Cita'
        context['list_url'] = self.success_url
        return context

class AppointmentByDoctorListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Appointment
    template_name = 'appointment/appointments.html'
    permission_required = 'appointment.view_appointment'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            id = request.POST['id']
            if action == 'searchdata':
                data = []
                for appointment in Appointment.objects.filter(doctor__pk = id):
                    data.append(appointment.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Citas por Doctor'
        context['create_url'] = reverse_lazy('appointment:appointment_create')
        context['list_url'] = reverse_lazy('appointment:appointment_list')
        context['entity'] = 'Citas'
        context['form'] = AppointmentByDoctorForm()
        return context

class AppointmentByPatientListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Appointment
    template_name = 'appointment/appointments-by-patient.html'
    permission_required = 'appointment.view_appointment'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            id = request.POST['id']
            if action == 'searchdata':
                data = []
                for appointment in Appointment.objects.filter(patient__pk = id):
                    print(appointment)
                    data.append(appointment.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Citas por Paciente'
        context['create_url'] = reverse_lazy('appointment:appointment_create')
        context['list_url'] = reverse_lazy('appointment:appointment_list')
        context['entity'] = 'Citas'
        context['form'] = AppointmentByPatientForm()
        return context