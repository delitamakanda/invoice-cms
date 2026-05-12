import { authAxios } from '@/utils/auth.js'

export function prepareInvoice(invoiceId) {
    return authAxios.post(
        `api/v1/invoices/${invoiceId}/prepare_electronic_invoice/`,
    )
}

export function sendInvoice(invoiceId) {
    return authAxios.post(
        `api/v1/invoices/${invoiceId}/send_electronic_invoice/`,
    )
}

export function getInvoiceStatus(invoiceId) {
    return authAxios.get(
        `api/v1/invoices/${invoiceId}/get_invoice_status/`,
    )
}