from django.urls import path
from .views import *

app_name = 'patient'

urlpatterns = [
    path('list/',PatientListView.as_view(),name='patient_list'),
    path('create/',PatientCreateView.as_view(),name='patient_create'),
    path('update/<int:pk>/',PatientUpdateView.as_view(),name='patient_update'),
    path('delete/<int:pk>/',PatientDeleteView.as_view(),name='patient_delete'),
]

