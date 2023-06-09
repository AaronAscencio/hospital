from django.urls import path
from .views.category.views import *
from .views.product.views import *

app_name = 'product'

urlpatterns = [
    path('category/list/',CategoryListView.as_view(),name="category_list"),
    path('category/add/',CategoryCreateView.as_view(),name="category_create"),
    path('category/update/<int:pk>/',CategoryUpdateView.as_view(),name="category_update"),
    path('category/delete/<int:pk>/',CategoryDeleteView.as_view(),name="category_delete"),

    path('list/',ProductListView.as_view(),name="product_list"),
    path('add/',ProductCreateView.as_view(),name="product_create"),
    path('delete/<int:pk>/',ProductDeleteView.as_view(),name="product_delete"),
    path('update/<int:pk>/',ProductUpdateView.as_view(),name="product_update"),
]

