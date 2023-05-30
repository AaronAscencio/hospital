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
from .models import Nurse
from .forms import NurseForm

class NurseListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Nurse
    template_name = 'nurse/list.html'
    permission_required = 'nurse.view_nurse'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Nurse.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Enfermeras'
        context['create_url'] = reverse_lazy('nurse:nurse_create')
        context['list_url'] = reverse_lazy('nurse:nurse_list')
        context['entity'] = 'Enfermeras'
        return context
    
class NurseCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = Nurse
    form_class = NurseForm
    template_name = 'nurse/create.html'
    permission_required = 'nurse.add_nurse'
    success_url = reverse_lazy('nurse:nurse_list')
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
        context['title'] = 'Creación de una Enfermera'
        context['entity'] = 'Enfermeras'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class NurseUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Nurse
    form_class = NurseForm
    template_name = 'nurse/create.html'
    success_url = reverse_lazy('nurse:nurse_list')
    permission_required = 'nurse.change_nurse'
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
        context['title'] = 'Edición de una Enfermera'
        context['entity'] = 'Enfermeras'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class NurseDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    
    model = Nurse
    template_name = 'nurse/delete.html'
    success_url = reverse_lazy('nurse:nurse_list')
    permission_required = 'nurse.delete_nurse'
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
        context['title'] = 'Eliminación de una Enfermera'
        context['entity'] = 'Enfermeras'
        context['list_url'] = self.success_url
        return context