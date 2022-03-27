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
  </div>
</template>

<script>
import { authAxios } from '../../../utils/auth'
import { defineComponent, reactive } from 'vue'
import { useRoute } from 'vue-router'

export default defineComponent ({
    setup() {

        const state = reactive({
            client: {},
        })

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
        }
    }
})
</script>

<style scoped>
.demo-page-header :deep(tr:last-child td) {
  padding-bottom: 0;
}
</style>