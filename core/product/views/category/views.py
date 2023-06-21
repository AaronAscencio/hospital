from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,FormView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from core.user.mixins import ValidatePermissionRequiredMixin
from core.product.models import Category
from core.product.forms import CategoryForm

class CategoryListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    permission_required = 'product.view_category'
    model = Category
    template_name = 'category/list.html'

    @method_decorator(csrf_exempt)
    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Category.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Categorías'
        context['create_url'] = reverse_lazy('product:category_create')
        context['list_url'] = reverse_lazy('product:category_list')
        context['entity'] = 'Categorias'
        return context

class CategoryCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    permission_required = 'product.add_category'
    model = Category
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = reverse_lazy('product:category_list')

    def get_context_data(self,**kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Creacion de una categoria'
        context['entity'] = 'Categorias'
        context['list_url'] = reverse_lazy('product:category_list')
        context['action'] = 'add'
        return context


    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    def post(self,request,*args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if(action=='add'):
                form = self.get_form()
                if (form.is_valid()):
                    form.save()
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No se ha enviado ninguna accion'
        except Exception as e:
            data['error'] = str(e)
            
        return JsonResponse(data)

class CategoryUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = reverse_lazy('product:category_list')
    permission_required = 'product.change_category'

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    


    def post(self,request,*args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if(action=='edit'):
                form = self.get_form()
                form = form.save()
            else:
                data['error'] = 'No se ha enviado ninguna accion'
        except Exception as e:
            data['error'] = str(e)
            
        return JsonResponse(data)




    def get_context_data(self,**kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Modificacion  de una categoria'
        context['entity'] = 'Categorias'
        context['list_url'] = reverse_lazy('product:category_list')
        context['action'] = 'edit'
        return context

class CategoryDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView): 
    permission_required = 'product.delete_category'
    model = Category
    template_name = 'category/delete.html'
    success_url = reverse_lazy('product:category_list')


    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self,**kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion  de una categoria'
        context['entity'] = 'Categorias'
        context['list_url'] = reverse_lazy('product:category_list')
        return context

    def post(self,request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        
        return JsonResponse(data)