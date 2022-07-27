from rest_framework import serializers

from .models import Client
from apps.invoice.models import Invoice

class ClientInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = (
            'id',
            'invoice_number',
            'is_sent',
            'is_paid',
            'gross_amount',
            'vat_amount',
            'net_amount',
            'get_due_date_formatted',
            'invoice_type',
            'is_credited',
        )

class ClientSerializer(serializers.ModelSerializer):
    invoices = ClientInvoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        read_only_fields = (
            'created_by',
            'created_at',
        )
        fields = (
            'id',
            'name',
            'email',
            'org_number',
            'address1',
            'address2',
            'zip_code',
            'place',
            'country',
            'contact_person',
            'contact_reference',
            'created_by',
            'created_at',
            'invoices',
        )