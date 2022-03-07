<template>
  <div class="page-signin">
    <h1>Sign in</h1>

    <a-form
    layout="inline"
    :model="formState"
    @finish="handleFinish"
    @finishFailed="handleFinishFailed"
  >
    <a-form-item>
      <a-input v-model:value="formState.username" type="email" placeholder="E-mail">
        <template #prefix><UserOutlined style="color: rgba(0, 0, 0, 0.25)" /></template>
      </a-input>
    </a-form-item>
    <a-form-item>
      <a-input v-model:value="formState.password" type="password" placeholder="Password" autocomplete="off">
        <template #prefix><LockOutlined style="color: rgba(0, 0, 0, 0.25)" /></template>
      </a-input>
    </a-form-item>
    <a-form-item>
      <a-button
        type="primary"
        html-type="submit"
        :disabled="formState.user === '' || formState.password === ''"
      >
        Log in
      </a-button>
    </a-form-item>
  </a-form>
  </div>
</template>

<script>
import { UserOutlined, LockOutlined } from '@ant-design/icons-vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { defineComponent, reactive } from 'vue'
import { message } from 'ant-design-vue'
import axios from 'axios'

export default defineComponent ({
  setup() {
    const router = useRouter()
    const store = useStore()
    const formState = reactive({
      username: '',
      password: ''
    })

    const errorMessage = (verb) => {
      message.error(verb);
    };

    const handleFinish = values => {
      console.log(values, formState)
      axios.post('/api/v1/token/login/', { username: formState.username, password: formState.password})
        .then(response => {
          const token = response.data.auth_token
          store.commit('user/setToken', token)
          localStorage.setItem('token', token)
          router.push('/dashboard/my-account')
        })
        .catch(error => {
          if (error.response) {
            for(const property in error.response.data) {
              errorMessage(`${property}: ${error.response.data[property]}`)
            }
            console.log(JSON.stringify(error.response.data))
          } else if (error.message) {
            console.log(JSON.stringify(error.message))
          } else {
            console.log(JSON.stringify(error))
          }
        })
    }

    const handleFinishFailed = errors => {
      console.log(errors)
    }

    return {
      formState,
      handleFinish,
      handleFinishFailed,
      errorMessage,
      router,
      store,
    }
  },
  components: {
    UserOutlined,
    LockOutlined
  }
})
</script>
