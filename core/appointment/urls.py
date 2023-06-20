from django.urls import path
from .views import *

app_name = 'appointment'

urlpatterns = [
    path('list/',AppointmentListView.as_view(),name='appointment_list'),
    path('create/',AppointmentCreateView.as_view(),name='appointment_create'),
    path('update/<int:pk>/',AppointmentUpdateView.as_view(),name='appointment_update'),
    path('delete/<int:pk>/',AppointmentDeleteView.as_view(),name='appointment_delete'),
    path('list-by-doctor/',AppointmentByDoctorListView.as_view(),name='appointment_by_doctor_list'),
    path('list-by-patient/',AppointmentByPatientListView.as_view(),name='appointment_by_patient_list'),
]

