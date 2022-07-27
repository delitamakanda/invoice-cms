from rest_framework import serializers

from .models import Invoice, Item

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        read_only_fields = (
            'invoice',
        )
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
    items = ItemSerializer(many=True)
    bankaccount = serializers.CharField(required=False)

    class Meta:
        model = Invoice
        read_only_fields = (
            'team',
            'invoice_number',
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
            'is_credit_for',
            'is_credited',
            'is_sent',
            'is_paid',
            'bankaccount',
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
            'items',
            'get_due_date_formatted',
        )
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = Invoice.objects.create(**validated_data)

        for item in items_data:
            Item.objects.create(invoice=invoice, **item)

        return invoice
