<template>
  <div class="page-clients">
      <h1>Clients</h1>

      <router-link :to="{name: 'addClient' }"><a-button style="margin-bottom: 16px" type="primary">Add client</a-button></router-link>

      <a-table :columns="columns" :row-key="record => record.id" :data-source="state.clients">
    <template #name="{ record }">
      <router-link :to="{ name: 'client', params: { id: record.id }}">{{ record.name }}</router-link>
    </template>
    <template #customTitle>
      <span>
        <smile-outlined />
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
    <!-- <template #action="{ record }">
      <span>
        <a>Delete 一 {{ record.name }}</a>
        <a-divider type="vertical" />
        <a class="ant-dropdown-link">
          More actions
          <down-outlined />
        </a>
      </span>
    </template> -->
  </a-table>
  </div>
</template>

<script>
import { authAxios } from '../../../utils/auth'
import { SmileOutlined, DownOutlined } from '@ant-design/icons-vue'
import { defineComponent, reactive } from 'vue'

const columns = [
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
  {
    title: 'Address',
    key: 'address1',
    dataIndex: 'address1'
  },
];

export default defineComponent ({
    setup() {

        const state = reactive({
            clients: [],
        })

        authAxios.get('api/v1/clients/')
            .then(response => {
                for(let i = 0; i< response.data.length;i++) {
                    state.clients.push(response.data[i])
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
    components: {
        SmileOutlined,
        DownOutlined,
    }
})
</script>

<style>

</style>