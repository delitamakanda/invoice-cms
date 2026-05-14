import random
import uuid


class MockTaxReportingService:
    def send_tax_report(self, payload: dict) -> dict:
        scenario = random.choice([
            'ACCEPTED',
            'REJECTED',
            'FAILED',
            'ACCEPTED',
            'ACCEPTED',
            'ACCEPTED',
            'REJECTED',
        ])
        
        if scenario == 'FAILED':
            return {
                'e_reporting_status': 'FAILED',
                'e_reporting_reference': None,
                'error': 'Internal server error',
            }
        if scenario == 'REJECTED':
            return {
                'e_reporting_status': 'REJECTED',
                'e_reporting_reference': f"REPORT_{uuid.uuid4()}",
                'e_reporting_rejection_reason': 'Invalid client data',
            }
        return {
            'e_reporting_status': 'ACCEPTED',
            'e_reporting_reference': f"REPORT_{uuid.uuid4()}",
            'message': "data e-reporting sent successfully",
        }
        