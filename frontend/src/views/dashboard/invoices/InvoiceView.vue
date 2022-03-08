<template>
  <div class="page-invoice">
    <a-page-header
      class="demo-page-header"
      style="border: 1px solid rgb(235, 237, 240)"
      :title="'Invoice ' + state.invoice.invoice_number"
      sub-title="Invoice details"
      @back="() => $router.go(-1)"
    >
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
        :data-source="state.items"
        :rowClassName="(record, index) => (index % 2 === 1 ? 'table-striped' : null)"
    />

  </div>
</template>

<script>
import { authAxios } from '../../../utils/auth'
import { defineComponent, reactive } from 'vue'
import { useRoute } from 'vue-router'

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
            items: []
        })

        const route = useRoute()

        authAxios.get(`api/v1/invoices/${route.params.id}/`)
            .then(response => {
                state.invoice = response.data
            })
            .catch(error => {
                console.log(JSON.stringify(error))
            })

        authAxios.get(`api/v1/items/?invoice_id=${route.params.id}`)
            .then(response => {
                for(let i = 0; i< response.data.length;i++) {
                    state.items.push(response.data[i])
                }
            })
            .catch(error => {
                console.log(JSON.stringify(error))
            })


        return {
            state,
            route,
            columns,
        }
    }
})
</script>

<style scoped>
.demo-page-header :deep(tr:last-child td) {
  padding-bottom: 0;
}
</style>