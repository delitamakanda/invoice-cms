from cgitb import lookup
from django.shortcuts import render

from django.core.exceptions import PermissionDenied

from rest_framework import viewsets

from .models import Invoice, Item

from .serializers import InvoiceSerializer, ItemSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        team = self.request.user.teams.first()
        invoice_number = team.first_invoice_number
        team.first_invoice_number = invoice_number + 1
        team.save()
        serializer.save(created_by=self.request.user, team=team, modified_by=self.request.user, invoice_number=invoice_number)

    def perform_update(self, serializer):
        obj = self.get_object()

        if self.request.user != obj.created_by:
            raise PermissionDenied('Wrong object !')
        serializer.save()


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def get_queryset(self):
        invoice_id = self.request.GET.get('invoice_id', 0)
        return self.queryset.filter(invoice__id=invoice_id)

    def perform_create(self, serializer):
        pass

    def perform_update(self, serializer):
        pass
