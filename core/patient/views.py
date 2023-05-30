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
from .models import Patient
from .forms import PatientForm
from django.db import connection

class PatientListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Patient
    template_name = 'patient/list.html'
    permission_required = 'patient.view_patient'
    

    def patient_age_view(self, patient_id):
        query = f"SELECT dbo.GetPatientAge({patient_id}) AS age"
        with connection.cursor() as cursor:
            cursor.execute(query)
            age = cursor.fetchone()[0]
        return age

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Patient.objects.all():
                    i = i.toJSON()
                    pk = i['id']
                    i['age'] = self.patient_age_view(pk)
                    data.append(i)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Pacientes'
        context['create_url'] = reverse_lazy('patient:patient_create')
        context['list_url'] = reverse_lazy('patient:patient_list')
        context['entity'] = 'Pacientes'
        return context
    
class PatientCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patient/create.html'
    permission_required = 'patient.add_patient'
    success_url = reverse_lazy('patient:patient_list')
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
        context['title'] = 'Creación de un Paciente'
        context['entity'] = 'Pacientes'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class PatientUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patient/create.html'
    success_url = reverse_lazy('patient:patient_list')
    permission_required = 'patient.change_patient'
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
        context['title'] = 'Edición de un Paciente'
        context['entity'] = 'Pacientes'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class PatientDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    
    model = Patient
    template_name = 'patient/delete.html'
    success_url = reverse_lazy('patient:patient_list')
    permission_required = 'patient.delete_patient'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
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
        context['title'] = 'Eliminación de un Paciente'
        context['entity'] = 'Pacientes'
        context['list_url'] = self.success_url
        return context