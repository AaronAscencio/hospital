from django.urls import path
from .views import *

app_name = 'doctor'

urlpatterns = [
    path('list/',DoctorListView.as_view(),name='doctor_list'),
    path('create/',DoctorCreateView.as_view(),name='doctor_create'),
    path('update/<int:pk>/',DoctorUpdateView.as_view(),name='doctor_update'),
    path('delete/<int:pk>/',DoctorDeleteView.as_view(),name='doctor_delete'),
]

