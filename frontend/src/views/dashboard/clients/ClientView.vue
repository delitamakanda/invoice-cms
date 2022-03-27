<template>
  <div class="page-client">

    <a-breadcrumb>
    <a-breadcrumb-item><router-link to="/dashboard">Dashboard</router-link></a-breadcrumb-item>
    <a-breadcrumb-item><router-link to="/dashboard/clients">Clients</router-link></a-breadcrumb-item>
    <a-breadcrumb-item aria-current="true"><router-link :to="{ name: 'client', params: { id: route.params.id }}">{{state.client.name}}</router-link></a-breadcrumb-item>
  </a-breadcrumb>

    <a-page-header
      class="demo-page-header"
      style="border: 1px solid rgb(235, 237, 240)"
      :title="state.client.name"
      sub-title="Contact details"
      @back="() => $router.go(-1)"
    >
      <template #extra>
        <router-link :to="{ name: 'editClient', params: { id: route.params.id }}">
          <a-button key="3">Edit</a-button>
        </router-link>
        <a-button key="2">Delete</a-button>
        <a-button key="1" type="primary">Send</a-button>
      </template>
      <a-descriptions size="small" :column="3">
        <a-descriptions-item label="Name">{{state.client.name}}</a-descriptions-item>
        <a-descriptions-item v-if="state.client.address1" label="Address">
          {{state.client.address1}}
        </a-descriptions-item>
        <a-descriptions-item v-if="state.client.address2" label="Address 2">
          {{state.client.address2}}
        </a-descriptions-item>
        <a-descriptions-item v-if="state.client.zip_code || state.client.place" label="Zip code">
          {{state.client.zip_code}} {{state.client.place}}
        </a-descriptions-item>
        <a-descriptions-item v-if="state.client.country" label="Country">
          {{state.client.country}}
        </a-descriptions-item>
      </a-descriptions>
    </a-page-header>

    <div v-if="unpaidInvoices.length">
      <div>
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
    </div>
    <div v-if="paidInvoices.length">
      <div>
        <h2>Paid invoices</h2>
        <a-table
        class="ant-table-striped"
        size="middle"
        :columns="columns"
        :row-key="record => record.id" 
        :data-source="paidInvoices"
        :rowClassName="(record, index) => (index % 2 === 1 ? 'table-striped' : null)"
    >
    <template #action="{ record }">
      <span>
        <router-link :to="{ name: 'invoice', params: { id: record.id }}">details</router-link>
      </span>
    </template>
        </a-table>
      </div>
    </div>
  </div>
</template>

<script>
import { authAxios } from '../../../utils/auth'
import { defineComponent, reactive, computed } from 'vue'
import { useRoute } from 'vue-router'

const columns = [
  {
    title: '#',
    dataIndex: 'id',
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

export default defineComponent ({
    setup() {

        const state = reactive({
            client: {
              invoices: []
            },
        })

        const unpaidInvoices = computed(() => state.client.invoices.filter(invoice => invoice.is_paid === false))
        
        const paidInvoices = computed(() => state.client.invoices.filter(invoice => invoice.is_paid === true))

        const route = useRoute()

        authAxios.get(`api/v1/clients/${route.params.id}`)
            .then(response => {
                state.client = response.data
            })
            .catch(error => {
                console.log(JSON.stringify(error))
            })


        return {
            state,
            route,
            unpaidInvoices,
            paidInvoices,
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