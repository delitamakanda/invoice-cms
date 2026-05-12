from django.db import router
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import InvoiceViewSet, generate_pdf, send_reminder, prepare_electronic_invoice, send_electronic_invoice, get_invoice_status

router = DefaultRouter()

router.register('invoices', InvoiceViewSet, basename='invoices')

urlpatterns = [
    path('', include(router.urls)),
    path('invoices/<int:invoice_id>/generate_pdf/', generate_pdf, name='generate_pdf'),
    path('invoices/<int:invoice_id>/send_reminder/', send_reminder, name='send_reminder'),
    
    path('invoices/<int:invoice_id>/prepare_electronic_invoice/', prepare_electronic_invoice, name='prepare_electronic_invoice'),
    path('invoices/<int:invoice_id>/send_electronic_invoice/', send_electronic_invoice, name='send_electronic_invoice'),
    path('invoices/<int:invoice_id>/get_invoice_status/', get_invoice_status, name='get_invoice_status'),
]
