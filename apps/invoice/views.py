import pdfkit

from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template

from rest_framework import viewsets, status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from apps.team.models import Team
from .models import Invoice, Item

from .serializers import InvoiceSerializer
from .services.invoicing_service import InvoiceService
from apps.invoice.services.e_reporting_service import EReportingService

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
        serializer.save(created_by=self.request.user, team=team, modified_by=self.request.user,
                        invoice_number=invoice_number, bankaccount=team.bankaccount)

    def perform_update(self, serializer):
        obj = self.get_object()

        if self.request.user != obj.created_by:
            raise PermissionDenied('Wrong object !')
        serializer.save()


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def generate_pdf(request, invoice_id):
    invoice = get_object_or_404(
        Invoice, pk=invoice_id, created_by=request.user)
    team = Team.objects.filter(created_by=request.user).first()
    template = get_template('pdf.html')
    if invoice.is_credit_for:
        template = get_template('pdf_creditnote.html')
    html = template.render({'invoice': invoice, 'team': team})
    pdf = pdfkit.from_string(html, False, options={})
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def send_reminder(request, invoice_id):
    invoice = get_object_or_404(
        Invoice, pk=invoice_id, created_by=request.user)
    team = Team.objects.filter(created_by=request.user).first()

    subject = f'Unpaid invoice'
    from_email = team.email
    to = [invoice.client.email]
    text_content = 'You have an unpaid invoice. Invoice number: # %s' % str(
        invoice.invoice_number)
    html_content = '<strong>You have an unpaid invoice</strong>. Invoice number: # %s' % str(
        invoice.invoice_number)

    message = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        to
    )
    message.attach_alternative(html_content, 'text/html')
    template = get_template('pdf.html')
    html = template.render({'invoice': invoice, 'team': team})
    pdf = pdfkit.from_string(html, False, options={})


    if pdf:
        name = 'invoice_%s.pdf' % invoice.invoice_number
        message.attach(name, pdf, 'application/pdf')

    message.send()

    return Response()

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def prepare_electronic_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, created_by=request.user)
    
    service = InvoiceService()
    invoice = service.prepare(invoice)
    
    return Response({
        'id': invoice.id,
        'electronic_status': invoice.electronic_status,
        'pdp_last_payload': invoice.pdp_last_payload,
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_electronic_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, created_by=request.user)
    service = InvoiceService()
    invoice = service.send(invoice)
    return Response({
        'id': invoice.id,
        'electronic_status': invoice.electronic_status,
        'pdp_last_response': invoice.pdp_last_response,
        'pdp_retry_count': invoice.pdp_retry_count,
        'pdp_reference': invoice.pdp_reference,
        'pdp_reject_reason': invoice.pdp_reject_reason,
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_invoice_status(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, created_by=request.user)
    return Response({
        'electronic_status': invoice.electronic_status,
        'id': invoice.id,
        'pdp_last_response': invoice.pdp_last_response,
        'pdp_retry_count': invoice.pdp_retry_count,
        'pdp_reference': invoice.pdp_reference,
        'pdp_reject_reason': invoice.pdp_reject_reason,
    })


@api_view(['POST'])
def prepare_e_reporting(request, pk):
    invoice = Invoice.objects.get(pk=pk, created_by=request.user)
    service = EReportingService()
    invoice = service.prepare(invoice)
    
    return Response({
        'id': invoice.id,
        'e_reporting_status': invoice.e_reporting_status,
        'e_reporting_required': invoice.e_reporting_required,
        'payload': invoice.e_reporting_last_payload,
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def send_e_reporting(request, pk):
    invoice = Invoice.objects.get(pk=pk, created_by=request.user)
    service = EReportingService()
    invoice = service.report(invoice)
    
    return Response({
        'id': invoice.id,
        'e_reporting_status': invoice.e_reporting_status,
        'e_reporting_reference': invoice.e_reporting_reference,
        'e_reporting_rejection_reason': invoice.e_reporting_rejection_reason,
        'e_reporting_retry_count': invoice.e_reporting_retry_count
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_e_reporting_status(request, pk):
    invoice = Invoice.objects.get(pk=pk, created_by=request.user)
    return Response({
        'id': invoice.id,
        'e_reporting_required': invoice.e_reporting_required,
        'e_reporting_last_response': invoice.e_reporting_last_response,
        'e_reporting_retry_count': invoice.e_reporting_retry_count,
        'e_reporting_last_payload': invoice.e_reporting_last_payload,
        'e_reporting_status': invoice.e_reporting_status,
        'e_reporting_reference': invoice.e_reporting_reference,
        'e_reporting_rejection_reason': invoice.e_reporting_rejection_reason,
    }, status=status.HTTP_200_OK)
