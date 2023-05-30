from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect

class LoginFormView(LoginView):
    template_name = 'login/login.html'


    def dispatch(self, request, *args, **kwargs):
        if(request.user.is_authenticated):
            return redirect('login:dashboard')
        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesion'
        return context 
    
class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard.html'