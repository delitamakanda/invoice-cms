<template>
  <div class="page-invoice">
    <a-page-header
      class="demo-page-header"
      style="border: 1px solid rgb(235, 237, 240)"
      :title="'Invoice ' + state.invoice.invoice_number"
      sub-title="Invoice details"
      @back="() => $router.go(-1)"
    >

      <a-button type="primary" @click="downloadPdf()">Download PDF</a-button>
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

  </div>
</template>

<script>
import { authAxios } from '../../../utils/auth'
import { defineComponent, reactive } from 'vue'
import { useRoute } from 'vue-router'
const fileDownload = require('js-file-download')

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
    title: 'Amount',
    dataIndex: 'net_amount',
  },
];

export default defineComponent ({
    setup() {

        const state = reactive({
            invoice: {},
        })

        const route = useRoute()

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

        return {
            state,
            route,
            columns,
            downloadPdf,
        }
    }
})
</script>

<style scoped>
.demo-page-header :deep(tr:last-child td) {
  padding-bottom: 0;
}
</style>