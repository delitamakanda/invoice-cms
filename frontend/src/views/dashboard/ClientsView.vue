<template>
  <div class="page-clients">
      <h1>Clients</h1>

      <a-table :columns="columns" :row-key="record => record.id" :data-source="state.clients">
    <template #name="{ text }">
      <span>{{ text }}</span>
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
    <template #action="{ record }">
      <span>
        <router-link :to="{ name: 'client', params: { id: record.id }}">Edit 一 {{ record.name }}</router-link>
        <a-divider type="vertical" />
        <a>Delete</a>
        <a-divider type="vertical" />
        <a class="ant-dropdown-link">
          More actions
          <down-outlined />
        </a>
      </span>
    </template>
  </a-table>
  </div>
</template>

<script>
import { authAxios } from '../../utils/auth'
import { SmileOutlined, DownOutlined } from '@ant-design/icons-vue'
import { defineComponent, reactive } from 'vue'

const columns = [
  {
    dataIndex: 'name',
    key: 'name',
    sorter: true,
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
    title: 'Action',
    key: 'action',
    slots: {
      customRender: 'action',
    },
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