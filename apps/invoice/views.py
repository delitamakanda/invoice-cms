import pdfkit

from django.shortcuts import render

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
