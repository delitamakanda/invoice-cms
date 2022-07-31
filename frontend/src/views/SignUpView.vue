<template>
  <div class="page-signup">
    <h1>Sign up</h1>

    <a-form
    name="custom-validation"
    ref="formRef"
    :model="formState"
    :rules="rules"
    v-bind="layout"
    @finish="handleFinish"
    @finishFailed="handleFinishFailed"
  >
    <a-form-item ref="username" label="E-mail" name="username">
      <a-input v-model:value="formState.username" />
    </a-form-item>
    <a-form-item ref="password1" has-feedback label="Password" name="password1">
      <a-input v-model:value="formState.password1" type="password" autocomplete="off" />
    </a-form-item>
    <a-form-item ref="password2" has-feedback label="Confirm" name="password2">
      <a-input v-model:value="formState.password2" type="password" autocomplete="off" />
    </a-form-item>
    <a-form-item :wrapper-col="{ span: 14, offset: 4 }">
      <a-button type="primary" html-type="submit">Submit</a-button>
      <a-button style="margin-left: 10px" @click="resetForm">Reset</a-button>
    </a-form-item>
  </a-form>
  <router-link to="sign-in">Sign in</router-link>
  </div>
</template>

<script>
import { defineComponent, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { message } from 'ant-design-vue'
import axios from 'axios'

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
    
    let validatePass = async (rule, value) => {
      if (value === '') {
        return Promise.reject('Please input the password');
      } else {
        if (formState.password2 !== '') {
          formRef.value.validateFields('password2');
        }
        return Promise.resolve();
      }
    };
    let validatePass2 = async (rule, value) => {
      if (value === '') {
        return Promise.reject('Please input the password again');
      } else if (value !== formState.password1) {
        return Promise.reject("Two inputs don't match!");
      } else {
        return Promise.resolve();
      }
    };

    const rules = {
      username: [
        { required: true, message: 'E-mail is required', trigger: 'blur' },
        { min: 1, max: 255, message: 'Length should be 3 to 5', trigger: 'blur' }
      ],
      password1: [{ required: true, validator: validatePass, trigger: 'change' }],
      password2: [{ validator: validatePass2, trigger: 'change' }],
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
    }
  }
})
</script>
