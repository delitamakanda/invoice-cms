<template>
  <div class="page-signin">
    <h1>Sign in</h1>

    <a-form
      :model="formState"
      name="basic"
      :label-col="{ span: 8 }"
      :wrapper-col="{ span: 16 }"
      autocomplete="off"
      @finish="handleFinish"
      @finishFailed="handleFinishFailed"
    >
      <a-form-item
        label="E-mail address"
        name="username"
        :rules="[{ required: true, message: 'Email is required' }]"
      >
        <a-input v-model:value="formState.username" />
      </a-form-item>

      <a-form-item
        label="Password"
        name="password"
        :rules="[{ required: true, message: 'Password is required' }]"
      >
        <a-input-password v-model:value="formState.password" />
      </a-form-item>

      <a-form-item name="remember" :wrapper-col="{ offset: 8, span: 16 }">
        <a-checkbox v-model:checked="formState.remember">Remember me</a-checkbox>
      </a-form-item>

      <a-form-item :wrapper-col="{ offset: 8, span: 16 }">
        <a-button type="primary" html-type="submit">Login</a-button>
      </a-form-item>
      Or
      <router-link to="/sign-up">Register now!</router-link>
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
      password: '',
      remember: true,
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
          router.push('/')
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
