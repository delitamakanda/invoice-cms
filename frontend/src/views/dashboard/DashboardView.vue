<template>
  <div class="page-dashboard">
    <h1>Dashboard</h1>

    <a-row :gutter="[16,8]">
     <a-col :span="12">
    <div v-if="unpaidInvoices.length">
        <h2>Unpaid invoices</h2>
        <a-table
        class="ant-table-striped"
        size="middle"
        :columns="columns"
        :row-key="record => record.id" 
        :data-source="unpaidInvoices"
        :rowClassName="(record, index) => (index % 2 === 1 ? 'table-striped' : null)"
    >
    <template #action="{ record }">
      <span>
        <router-link :to="{ name: 'invoice', params: { id: record.id }}">details</router-link>
      </span>
    </template>
        </a-table>
    </div>
  </a-col>
  <a-col :span="12">
    <div v-if="state.clients.length">
      <h2>Newest clients</h2>
    <a-table :columns="columns2" :row-key="record => record.id" :data-source="state.clients">
    <template #name="{ record }">
      <router-link :to="{ name: 'client', params: { id: record.id }}">{{ record.name }}</router-link>
    </template>
    <template #customTitle>
      <span>
        Name
      </span>
    </template>
    <template #email="{ text }">
      <span>
        {{ text }}
      </span>
    </template>
    <template #address1="{ text }">
      <span>
        {{ text }}
      </span>
    </template>
    <template #action="{ record }">
      <span>
        <a>Edit 一 {{ record.name }}</a>  
      </span>
    </template>
  </a-table>
    </div>
  </a-col>
</a-row>
  </div>
</template>

<script>
import { authAxios } from '@/utils/auth'
import { defineComponent, reactive, computed } from 'vue'

const columns2 = [
  {
    dataIndex: 'name',
    key: 'name',
    slots: {
      title: 'customTitle',
      customRender: 'name',
    },
  },
  {
    title: 'E-mail',
    dataIndex: 'email',
    key: 'email'
  },
];


const columns = [
  {
    title: '#',
    dataIndex: 'id',
  },
  {
    title: 'Client',
    dataIndex: 'client_name',
  },
  {
    title: 'Amount',
    dataIndex: 'net_amount',
  },
  {
    title: 'Due date',
    dataIndex: 'get_due_date_formatted',
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

export default defineComponent({
  setup() {

    const state = reactive({
      invoices: [],
      clients: []
    })

    const unpaidInvoices = computed(() => state.invoices.filter(invoice => invoice.is_paid === false))
        
    authAxios.get(`api/v1/invoices/`)
        .then(response => {
          for (let i = 0; i < response.data.length; i++) {
            if (!response.data[i].is_credit_for) {
              state.invoices.push(response.data[i])
            }
          }
        })
        .catch(error => {
            console.log(JSON.stringify(error))
        })

    authAxios.get(`api/v1/clients/`)
        .then(response => {
            for (let i = 0; i < response.data.length; i++) {
              if (state.clients.length <= 5) {
                state.clients.push(response.data[i])
              }
              
            }
        })
        .catch(error => {
            console.log(JSON.stringify(error))
        })


    return {
        state,
        columns,
        columns2,
        unpaidInvoices,
    }
  }
})
</script>
