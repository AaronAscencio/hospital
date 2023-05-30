from django.urls import path
from .views import *

app_name = 'nurse'

urlpatterns = [
    path('list/',NurseListView.as_view(),name='nurse_list'),
    path('create/',NurseCreateView.as_view(),name='nurse_create'),
    path('update/<int:pk>/',NurseUpdateView.as_view(),name='nurse_update'),
    path('delete/<int:pk>/',NurseDeleteView.as_view(),name='nurse_delete'),
]

