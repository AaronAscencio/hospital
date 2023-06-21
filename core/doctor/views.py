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
from .models import Doctor
from .forms import DoctorForm
from core.appointment.models import *
from django.contrib import messages

class DoctorListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Doctor
    template_name = 'doctor/list.html'
    permission_required = 'doctor.view_doctor'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Doctor.objects.all():
                    print(i.pk)
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Doctores'
        context['create_url'] = reverse_lazy('doctor:doctor_create')
        context['list_url'] = reverse_lazy('doctor:doctor_list')
        context['entity'] = 'Doctores'
        return context
    
class DoctorCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctor/create.html'
    permission_required = 'doctor.add_doctor'
    success_url = reverse_lazy('doctor:doctor_list')
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
        context['title'] = 'Creación de un Doctor'
        context['entity'] = 'Doctores'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class DoctorUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctor/create.html'
    success_url = reverse_lazy('doctor:doctor_list')
    permission_required = 'doctor.change_doctor'
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
        context['title'] = 'Edición de un Doctor'
        context['entity'] = 'Doctores'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class DoctorDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    
    model = Doctor
    template_name = 'doctor/delete.html'
    success_url = reverse_lazy('doctor:doctor_list')
    permission_required = 'doctor.delete_doctor'
    #url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        current_date = date.today()
        doctor_appointments = Appointment.objects.filter(doctor_id=self.object.pk,date__gte= current_date)
        if doctor_appointments.exists():
            messages.error(request,'No puedes eliminar a este doctor, ya que cuenta con consultas asignadas')
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
        context['title'] = 'Eliminación de un Doctor'
        context['entity'] = 'Doctores'
        context['list_url'] = self.success_url
        return context

