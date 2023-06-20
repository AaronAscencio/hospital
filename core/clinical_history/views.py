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
from .models import ClinicalHistory
from .forms import ClinicalHistoryByPatientForm

# Create your views here.
class ClinicalHistoryListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = ClinicalHistory
    template_name = 'clinical-history/list.html'
    permission_required = 'clinical_history.view_clinical_history'
    
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
                for history in ClinicalHistory.objects.filter(patient__pk = id):
                    print(history.toJSON())
                    data.append(history.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Historiales Clinicos'
        context['create_url'] = reverse_lazy('nurse:nurse_create')
        context['list_url'] = reverse_lazy('nurse:nurse_list')
        context['entity'] = 'Enfermeras'
        context['form'] = ClinicalHistoryByPatientForm()
        return context