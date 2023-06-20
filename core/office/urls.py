from django.urls import path
from .views import *

app_name = 'office'

urlpatterns = [
    path('list/',OfficeListView.as_view(),name='office_list'),
    path('create/',OfficeCreateView.as_view(),name='office_create'),
    path('update/<int:pk>/',OfficeUpdateView.as_view(),name='office_update'),
    path('delete/<int:pk>/',OfficeDeleteView.as_view(),name='office_delete'),
]

