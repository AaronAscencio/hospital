from django.forms.models import model_to_dict
from django.views.generic import ListView,CreateView,DeleteView,UpdateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from core.product.forms import ProductForm
from core.product.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from core.user.mixins import ValidatePermissionRequiredMixin

class ProductListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Product
    template_name = 'product/list.html'
    permission_required = 'product.view_product'


    @method_decorator(csrf_exempt)
    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        context['list_url'] = reverse_lazy('product:product_list')
        context['entity'] = 'Productos'
        context['create_url'] = reverse_lazy('product:product_create')
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Product.objects.all():
                    data.append(i.toJSON())
                    
                    
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class ProductCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('product:product_list')
    permission_required = 'product.add_product'

    def get_context_data(self,**kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Creacion de un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = reverse_lazy('product:product_list')
        context['action'] = 'add'
        
        return context


    #@method_decorator(login_required)
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


class ProductDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = Product
    template_name = 'product/delete.html'
    success_url = reverse_lazy('product:product_list')
    permission_required = 'product.delete_product'


    @method_decorator(login_required)
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
        context['title'] = 'Eliminación de un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = reverse_lazy('product:product_list')
        return context


class ProductUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('product:product_list')
    permission_required = 'product.change_product'


    @method_decorator(login_required)
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
        context['title'] = 'Edición de un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = reverse_lazy('product:product_list')
        context['action'] = 'edit'
        return context