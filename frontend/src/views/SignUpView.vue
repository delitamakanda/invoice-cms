<template>
  <div class="page-signup">
    <a-typography-title class="page-about-title">{{ $t("signupPage.title") }}</a-typography-title>
    <p>{{ $t("signupPage.baseline") }}  <router-link to="/sign-in">{{ $t("signupPage.loginButtonLabelKey") }}</router-link></p>

    <a-form
    name="custom-validation"
    ref="formRef"
    :model="formState"
    :rules="rules"
    v-bind="layout"
    @finish="handleFinish"
    @finishFailed="handleFinishFailed"
  >
    <a-form-item ref="username" :label="$t('signupPage.emailLabelKey')" name="username">
      <a-input v-model:value="formState.username" />
    </a-form-item>
    <a-form-item ref="password1" has-feedback :label="$t('signupPage.passwordLabelKey')" name="password1">
      <a-input-password v-model:value="formState.password1" />
    </a-form-item>
    <a-form-item ref="password2" has-feedback :label="$t('signupPage.confirmPasswordLabelKey')" name="password2">
      <a-input v-model:value="formState.password2" type="password" autocomplete="off" />
    </a-form-item>
    <a-form-item :wrapper-col="{ span: 14, offset: 4 }">
      <a-button type="primary" html-type="submit">{{ $t("signupPage.registerButtonLabelKey") }}</a-button>
      <a-button style="margin-left: 10px" @click="resetForm">{{ $t("signupPage.resetButtonLabelKey") }}</a-button>
    </a-form-item>
  </a-form>
  </div>
</template>

<script>
import { defineComponent, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { message } from 'ant-design-vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'

export default defineComponent ({
  setup() {
    const router = useRouter()
    const store = useStore()
    const formRef = ref()
    const formState = reactive({
      username: '',
      password1: '',
      password2: ''
    })
    const { t } = useI18n()
    
    let validatePass = async (rule, value) => {
      if (value === '') {
        return Promise.reject(t('rules.required.message', { field: t('signupPage.passwordLabelKey') }));
      } else {
        if (formState.password2 !== '') {
          formRef.value.validateFields('password2');
        }
        return Promise.resolve();
      }
    };
    let validatePass2 = async (rule, value) => {
      if (value === '') {
        return Promise.reject(t('rules.required.message', { field: t('signupPage.confirmPasswordLabelKey') }));
      } else if (value !== formState.password1) {
        return Promise.reject(t('rules.mismatch.message'));
      } else {
        return Promise.resolve();
      }
    };

    const rules = {
      username: [
        { required: true, message: t('rules.required.message', { field: t('signupPage.emailLabelKey') }), trigger: 'blur' },
        { min: 5, max: 255, message: t('rules.length.message', { field: t('signupPage.emailLabelKey'), length: 5 }), trigger: 'blur' }
      ],
      password1: [{ required: true, validator: validatePass, trigger: 'change' }],
      password2: [{ required: true, validator: validatePass2, trigger: 'change' }],
    }

    const layout = {
      labelCol: { span: 4 },
      wrapperCol: { span: 14 },
    };

    const errorMessage = (verb) => {
      message.error(verb);
    };

    const handleFinish = (values) => {
      console.log(values, formState)
      axios.post('/api/v1/users/', { username: formState.username, password: formState.password1})
        .then(response => {
          authLogin(formState.username, formState.password1);
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

    const authLogin = (username, password) => {
      axios.post('/api/v1/token/login/', { username: username, password: password})
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

    const handleFinishFailed = (errors) => {
      console.log(errors);
    };

    const resetForm = () => {
      formRef.value.resetFields()
    }

    return {
      formState,
      formRef,
      rules,
      layout,
      handleFinishFailed,
      handleFinish,
      resetForm,
      errorMessage,
      router,
      store,
      t,
    }
  }
})
</script>
