from django.db import transaction

from apps.client.models import Client
from apps.invoice.enums import ElectronicInvoiceStatus
from apps.invoice.services.mock_pdp_service import MockPDPService

class InvoiceService:
    def __init__(self):
        self.pdp = MockPDPService()
        
    def build_payload(self, invoice):
        client = invoice.client
        
        return {
            "id": str(invoice.id),
            "invoice_number": invoice.invoice_number,
            "client": {
                "id": str(client.id),
                "name": client.name,
                "siret": client.org_number,
                "email": client.email,
            },
            "amounts": {
                "total_ht": str(invoice.gross_amount),
                "total_tva": str(invoice.vat_amount),
                "total_ttc": str(invoice.net_amount),
            }
        }
    
    @transaction.atomic
    def prepare(self, invoice):
        payload = self.build_payload(invoice)
        invoice.electronic_status = ElectronicInvoiceStatus.READY_TO_SEND
        invoice.pdp_last_payload = payload
        invoice.save(update_fields=['electronic_status', 'pdp_last_payload', 'modified_at'])
        
        return invoice
    
    @transaction.atomic
    def send(self, invoice):
        payload = self.build_payload(invoice)
        response = self.pdp.send_invoice(payload)
        
        invoice.pdp_last_response = response
        invoice.pdp_last_payload = payload
        
        if response['electronic_status'] == ElectronicInvoiceStatus.ACCEPTED:
            invoice.electronic_status = ElectronicInvoiceStatus.ACCEPTED
            invoice.pdp_reference = response['pdp_reference']
            invoice.pdp_reject_reason = None
        elif response['electronic_status'] == ElectronicInvoiceStatus.REJECTED:
            invoice.electronic_status = ElectronicInvoiceStatus.REJECTED
            invoice.pdp_reference = response['pdp_reference']
            invoice.pdp_reject_reason = response['pdp_reject_reason']
        elif response['electronic_status'] == ElectronicInvoiceStatus.FAILED:
            invoice.electronic_status = ElectronicInvoiceStatus.FAILED
            invoice.pdp_retry_count +=1
            invoice.pdp_reject_reason = response['error']
        elif response['electronic_status'] == ElectronicInvoiceStatus.SENT:
            invoice.electronic_status = ElectronicInvoiceStatus.SENT
            invoice.pdp_reference = response['pdp_reference']
            invoice.pdp_reject_reason = None
        elif response['electronic_status'] == ElectronicInvoiceStatus.READY_TO_SEND:
            invoice.electronic_status = ElectronicInvoiceStatus.READY_TO_SEND
            invoice.pdp_reference = response['pdp_reference']
            invoice.pdp_reject_reason = None
        elif response['electronic_status'] == ElectronicInvoiceStatus.PDF_GENERATED:
            invoice.electronic_status = ElectronicInvoiceStatus.PDF_GENERATED
            invoice.pdp_reference = response['pdp_reference']
            invoice.pdp_reject_reason = None
        
        invoice.save(update_fields=[
            'electronic_status',
            'pdp_last_response',
            'pdp_last_payload',
            'pdp_reference',
            'pdp_reject_reason',
            'pdp_retry_count',
            'modified_at',
        ])
        
        return invoice