<template>
  <div class="page-signin">
    <a-typography-title class="page-about-title">{{ $t("signinPage.title") }}</a-typography-title>
    <p>{{ $t("signinPage.baseline") }}  <router-link to="/sign-up">{{ $t("signinPage.registerButtonLabelKey") }}</router-link></p>

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
        :label="$t('signinPage.emailLabelKey')"
        name="username"
        :rules="[{ required: true, message: $t('rules.required.message', { field: $t('signinPage.emailLabelKey') })}]"
      >
        <a-input v-model:value="formState.username" />
      </a-form-item>

      <a-form-item
        :label="$t('signinPage.passwordLabelKey')"
        name="password"
        :rules="[{ required: true, message: $t('rules.required.message', { field: $t('signinPage.passwordLabelKey') })}]"
      >
        <a-input-password v-model:value="formState.password" />
      </a-form-item>

      <a-form-item name="remember" :wrapper-col="{ offset: 8, span: 16 }">
        <a-checkbox v-model:checked="formState.remember">{{ $t("signinPage.rememberMeLabelKey") }}</a-checkbox>
      </a-form-item>

      <a-form-item :wrapper-col="{ offset: 8, span: 16 }">
        <a-button type="primary" html-type="submit">{{ $t("signinPage.btnSigninKey") }}</a-button>
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
      username: window.localStorage.getItem('username') || '',
      password: window.localStorage.getItem('password') || '',
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
          if (formState.remember) {
            localStorage.setItem('username', formState.username)
            localStorage.setItem('password', formState.password)
          }
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
