

from django.urls import path
from .views import *

app_name = 'sale'

urlpatterns = [ 

    #Sale
    path('add/',SaleCreateView.as_view(),name="sale_create"),
    path('list/',SaleListView.as_view(), name='sale_list'),
    path('delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('update/<int:pk>/', SaleUpdateView.as_view(), name='sale_update'),
    path('invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),
    path('total/',TotalSaleListView.as_view(),name='sale_total'),
    path('by-doctor/',SaleByDoctorListView.as_view(),name='sales_by_doctor')
]