from django.db import transaction
from apps.invoice.enums import EReportingStatus
from apps.invoice.services.mock_tax_reporting_service import MockTaxReportingService

class EReportingService:
    def __init__(self):
        self.tax_reporting = MockTaxReportingService()
        
    def is_required(self, invoice):
        client = invoice.client
        
        if getattr(client, 'is_business', False) is False:
            return True
        if getattr(client, 'country_code', 'FR') != 'FR':
            return True
        return False
    
    def build_payload(self, invoice):
        client = invoice.client
        
        return {
            "id": str(invoice.id),
            "invoice_number": invoice.invoice_number,
            "client": {
                "id": str(client.id),
                "name": client.name,
                "siret": client.org_number,
            },
            'amounts': {
                'total_ttc': invoice.gross_amount,
                'total_vat': invoice.vat_amount,
                'total_ht': invoice.net_amount,
            },
            "vat": {
                "rate": str(getattr(invoice, "vat_rate", "20.00")),
                "amount": str(invoice.vat_amount),
            }
        }
    
    def detect_operation_type(self, invoice):
        client = invoice.client
        
        if getattr(client, 'is_business', False) is False:
            return "B2C"
        if getattr(client, 'country_code', 'FR')!= 'FR':
            return "ALIEN_B2B"
        return "B2B"
    
    @transaction.atomic
    def prepare(self, invoice):
        required = self.is_required(invoice)
        
        invoice.e_reporting_required = required
        invoice.e_reporting_status = (
            EReportingStatus.READY
            if required
            else EReportingStatus.NOT_REQUIRED
        )
        if required:
            invoice.e_reporting_last_payload = self.build_payload(invoice)
        
        invoice.save(update_fields=['e_reporting_required', 'e_reporting_status', 'e_reporting_last_payload', 'modified_at'])
        
        return invoice
    
    @transaction.atomic
    def report(self, invoice):
        if not invoice.e_reporting_required:
            invoice.e_reporting_status = EReportingStatus.NOT_REQUIRED
            invoice.save(update_fields=['e_reporting_status', 'modified_at'])
            return invoice
        payload = self.build_payload(invoice)
        response = self.tax_reporting.send_tax_report(payload)
        
        invoice.e_reporting_last_response = response
        invoice.e_reporting_last_payload = payload
        
        if response['e_reporting_status'] == 'ACCEPTED':
            invoice.e_reporting_status = EReportingStatus.ACCEPTED
            invoice.e_reporting_reference = response['e_reporting_reference']
            invoice.e_reporting_rejection_reason = None
        elif response['e_reporting_status'] == 'REJECTED':
            invoice.e_reporting_status = EReportingStatus.REJECTED
            invoice.e_reporting_rejection_reason = response['e_reporting_rejection_reason']
            invoice.e_reporting_reference = response['e_reporting_reference']
        else:
            invoice.e_reporting_status = EReportingStatus.FAILED
            invoice.e_reporting_rejection_reason = response['error']
            invoice.e_reporting_retry_count += 1
        invoice.save(update_fields=['e_reporting_status', 'e_reporting_rejection_reason', 'e_reporting_retry_count', 'modified_at'])
        
        return invoice