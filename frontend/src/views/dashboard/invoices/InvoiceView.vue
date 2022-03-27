<template>
  <div class="page-invoice">

    <a-breadcrumb>
    <a-breadcrumb-item><router-link to="/dashboard">Dashboard</router-link></a-breadcrumb-item>
    <a-breadcrumb-item><router-link to="/dashboard/invoices">Invoices</router-link></a-breadcrumb-item>
    <a-breadcrumb-item aria-current="true"><router-link :to="{ name: 'invoice', params: { id: route.params.id }}">Invoice #{{state.invoice.invoice_number}}</router-link></a-breadcrumb-item>
  </a-breadcrumb>

    <a-page-header
      class="demo-page-header"
      style="border: 1px solid rgb(235, 237, 240)"
      :title="'Invoice ' + state.invoice.invoice_number"
      sub-title="Invoice details"
      @back="() => $router.go(-1)"
    >

      <div class="buttons">
        <a-button type="primary" @click="downloadPdf()">Download PDF</a-button>

        <template v-if="!state.invoice.is_credit_for && !state.invoice.is_credited">
        <a-button type="default" v-if="!state.invoice.is_paid" @click="setAsPaid()">Set as paid</a-button>
        <a-button type="ghost" v-if="!state.invoice.is_paid" @click="createCreditNote()">Create credit note</a-button>
        </template>
        <a-button type="default" v-if="!state.invoice.is_paid && !state.invoice.is_credit_for" @click="sendReminder()">Send reminder</a-button>
      </div>
      <a-descriptions size="small" :column="3">
        <a-descriptions-item label="Client">{{state.invoice.client_name}}</a-descriptions-item>
        <a-descriptions-item v-if="state.invoice.client_address1" label="Address">
          {{state.invoice.client_address1}}
        </a-descriptions-item>
        <a-descriptions-item v-if="state.invoice.client_address2" label="Address 2">
          {{state.invoice.client_address2}}
        </a-descriptions-item>
        <a-descriptions-item v-if="state.invoice.client_zip_code || state.invoice.client_place" label="Zip code">
          {{state.invoice.client_zip_code}} {{state.invoice.client_place}}
        </a-descriptions-item>
        <a-descriptions-item v-if="state.invoice.client_country" label="Country">
          {{state.invoice.client_country}}
        </a-descriptions-item>
      </a-descriptions>
    </a-page-header>

    <a-table
        class="ant-table-striped"
        size="middle"
        :columns="columns"
        :row-key="record => record.id" 
        :data-source="state.invoice.items"
        :rowClassName="(record, index) => (index % 2 === 1 ? 'table-striped' : null)"
    />

    <h3>Summary</h3>
    <a-row type="flex" justify="center" align="top">
      <a-col :span="12">
        <p><strong>Net amount</strong> {{ state.invoice.net_amount }}</p>
        <p><strong>Vat amount</strong> {{ state.invoice.vat_amount }}</p>
        <p><strong>Gross amount</strong> {{ state.invoice.gross_amount }}</p>
        <p><strong>Bank account</strong> {{ state.invoice.bankaccount }}</p>
      </a-col>
      <a-col :span="12">
        <p><strong>Our reference</strong> {{ state.invoice.sender_reference }}</p>
        <p><strong>Client reference</strong> {{ state.invoice.client_contact_reference }}</p>
        <p><strong>Due date</strong> {{ state.invoice.get_due_date_formatted }}</p>
        <p><strong>Status</strong> {{ getStatusLabel(state.invoice) }}</p>
        <p><strong>Invoice type</strong> {{ getInvoiceType(state.invoice) }}</p>
      </a-col>
    </a-row>

  </div>
</template>

<script>
import { authAxios } from '../../../utils/auth'
import { defineComponent, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
const fileDownload = require('js-file-download')
import { message } from 'ant-design-vue'

const columns = [
  {
    title: '#',
    dataIndex: 'id',
  },
  {
    title: 'Title',
    dataIndex: 'title',
  },
  {
    title: 'Quantity',
    dataIndex: 'quantity',
  },
  {
    title: 'Vat rate',
    dataIndex: 'vat_rate',
  },
  {
    title: 'Total',
    dataIndex: 'net_amount',
  },
];

export default defineComponent ({
    setup() {

        const state = reactive({
            invoice: {},
        })

        const route = useRoute()
        const router = useRouter()

        authAxios.get(`api/v1/invoices/${route.params.id}/`)
            .then(response => {
                state.invoice = response.data
            })
            .catch(error => {
                console.log(JSON.stringify(error))
            })

        const downloadPdf = () => {
          authAxios.get(`/api/v1/invoices/${route.params.id}/generate_pdf/`, { responseType: 'blob', timeout: 30000})
            .then(response => {
              fileDownload(response.data, `invoice_${route.params.id}.pdf`)
            })
            .catch(error => {
              console.log(JSON.stringify(error))
            })
        }

        const sendReminder = () => {
          authAxios.get(`/api/v1/invoices/${route.params.id}/send_reminder/`, { timeout: 30000})
            .then(response => {
              // todo
            })
            .catch(error => {
              console.log(JSON.stringify(error))
            })
        } 

        const setAsPaid = async () => {
          state.invoice.is_paid = true
          let items = state.invoice.items;
          delete state.invoice['items']

          await authAxios.patch(`/api/v1/invoices/${route.params.id}/`, state.invoice)
            .then(response => {
               message.success(`Invoice ${response.data.invoice_number} is paid`)
            })
            .catch(error => {
              console.log(JSON.stringify(error))
            })
          
          state.invoice.items = items
        } 

        const createCreditNote = async () => {
          state.invoice.is_credited = true

          let items = state.invoice.items;
          delete state.invoice['items']

          await authAxios.patch(`/api/v1/invoices/${route.params.id}/`, state.invoice)
            .then(response => {
               message.success(`Invoice ${response.data.invoice_number} successfully changed`)
            })
            .catch(error => {
              console.log(JSON.stringify(error))
            })

          state.invoice.items = items
          
          let creditNote = state.invoice
          creditNote.is_credit_for = state.invoice.id
          creditNote.is_credited = false
          creditNote.invoice_type = 'credit_note'

          delete creditNote['id']

          await authAxios.post(`/api/v1/invoices/`, creditNote)
            .then(response => {
               message.success(`Credit note ${response.data.invoice_number} successfully added`)
               router.push('/dashboard/invoices')
            })
            .catch(error => {
              console.log(JSON.stringify(error))
            })

        } 

        return {
            state,
            route,
            router,
            columns,
            downloadPdf,
            setAsPaid,
            createCreditNote,
            sendReminder,
        }
    },
    methods: {
        getStatusLabel(invoice) {
            if (invoice.is_paid) {
                return 'Paid'
            } else {
                return 'Not paid'
            }
        },
        getInvoiceType(invoice) {
            if (invoice.invoice_type === 'invoice') {
                return 'Invoice'
            } else {
                return 'Credit note'
            }
        },
        getItemTotal(item) {
            const unit_price = item.unit_price
            const quantity = item.quantity
            const total = item.net_amount + (item.net_amount * (item.vat_rate / 100))
            return parseFloat(total).toFixed(2)
        }
    }
})
</script>

<style scoped>
.demo-page-header :deep(tr:last-child td) {
  padding-bottom: 0;
}
</style>