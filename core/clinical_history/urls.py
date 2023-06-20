from django.urls import path
from .views import *

app_name = 'clinical_history'

urlpatterns = [
    path('list/',ClinicalHistoryListView.as_view(),name='clinical_history_list')
]
