import random
import uuid

class MockPDPService:
    def send_invoice(self, payload: dict) -> dict:
        scenario = random.choice([
            'ACCEPTED',
            'REJECTED',
            'FAILED',
            'ACCEPTED',
            'ACCEPTED',
            'DRAFT',
            'ACCEPTED',
            'SENT',
            'READY_TO_SEND',
            'PDF_GENERATED',
            'ACCEPTED',
            'ACCEPTED',
        ])
        if scenario == 'FAILED':
            return {
                'electronic_status': 'FAILED',
                'pdp_reference': None,
                'error': 'Timeout error',
            }
        if scenario == 'REJECTED':
            return {
                'electronic_status': 'REJECTED',
                'pdp_reference': f'PDP-{uuid.uuid4()}',
                'pdp_reject_reason': 'Invalid invoice data',
            }
        
        if scenario == 'SENT' or scenario == 'READY_TO_SEND' or scenario == 'PDF_GENERATED':
            return {
                'electronic_status': 'SENT',
                'pdp_reference': f'PDP-{uuid.uuid4()}',
                'message': None,
            }
        return {
            'electronic_status': 'ACCEPTED',
            'pdp_reference': f'PDP-{uuid.uuid4()}',
            'message': 'Invoice sent successfully',
        }
        