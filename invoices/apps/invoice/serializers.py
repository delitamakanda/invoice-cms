from rest_framework import serializers

from .models import Invoice, Item

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = (
            'id',
            'invoice',
            'title',
            'quantity',
            'unit_price',
            'net_amount',
            'vat_rate',
            'discount',
        )


class InvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        read_only_fields = (
            'team',
            'created_by',
            'modified_by',
            'created_at',
            'modified_at',
        )
        fields = (
            'id',
            'invoice_number',
            'client_name',
            'client_email',
            'client_org_number',
            'client_address1',
            'client_address2',
            'client_zip_code',
            'client_place',
            'client_country',
            'client_contact_person',
            'client_contact_reference',
            'sender_reference',
            'invoice_type',
            'due_days',
            'is_credit_for'
            'is_sent',
            'gross_amount',
            'vat_amount',
            'net_amount',
            'discount_amount',
            'team',
            'client',
            'created_by',
            'modified_by',
            'created_at',
            'modified_at',
        )