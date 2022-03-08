<template>
  <div class="page-invoices">
      <h1>Invoices</h1>

      <!-- <router-link :to="{name: 'addClient' }"><a-button style="margin-bottom: 16px" type="primary">Add client</a-button></router-link> -->

      <a-table :columns="columns" :row-key="record => record.invoice_number" :data-source="state.invoices">
    <template #invoice_number="{ record }">
      <router-link :to="{ name: 'invoice', params: { id: record.id }}">{{ record.id }}</router-link>
    </template>
    <template #customTitle>
      <span>
       #
      </span>
    </template>
    <template #client="{ text }">
      <span>
        {{ text }}
      </span>
    </template>
    <template #gross_amount="{ record }">
      <span>
        {{ $filters.currency(+record.gross_amount) }}
      </span>
    </template>
    <template #Amount>
      <span>Amount</span>
    </template>
    <template #is_paid="{ record }">
      {{getStatusLabel(record)}}
    </template>
    <template #isPaid>
      <span>
        Is paid
      </span>
    </template>
    <!-- <template #action="{ record }">
      <span>
        <a>Delete 一 {{ record.client_name }}</a>
      </span>
    </template> -->
  </a-table>
  </div>
</template>

<script>
import { authAxios } from '../../../utils/auth'
import { defineComponent, reactive } from 'vue'

const columns = [
  {
    dataIndex: 'invoice_number',
    key: 'invoice_number',
    slots: {
      title: 'customTitle',
      customRender: 'invoice_number',
    },
  },
  {
    title: 'Client',
    dataIndex: 'client_name',
    key: 'client_name'
  },
  {
    key: 'gross_amount',
    dataIndex: 'gross_amount',
    slots: {
      title: 'Amount',
      customRender: 'gross_amount',
    },
  },
  {
    key: 'is_paid',
    dataIndex: 'is_paid',
    slots: {
      title: 'isPaid',
      customRender: 'is_paid',
    },
  },
  {
    title: '',
    key: 'action',
    dataIndex: 'action',
    slots: {
      customRender: 'action',
    },
  },
];

export default defineComponent ({
    setup() {

        const state = reactive({
            invoices: [],
        })

        authAxios.get('api/v1/invoices/')
            .then(response => {
                for(let i = 0; i< response.data.length;i++) {
                    state.invoices.push(response.data[i])
                }
            })
            .catch(error => {
                console.log(JSON.stringify(error))
            })


        return {
            columns,
            state,
        }
    },
    methods: {
        getStatusLabel(invoice) {
            if (invoice.is_paid) {
                return 'Yes'
            } else {
                return 'No'
            }
        }
    }
})
</script>

<style>

</style>