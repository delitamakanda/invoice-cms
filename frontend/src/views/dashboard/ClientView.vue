<template>
  <div class="page-clients">
      <h1>{{ state.client.name }}</h1>

      
  </div>
</template>

<script>
import { authAxios } from '../../utils/auth'
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

<style>

</style>