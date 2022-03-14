<template>
  <div class="page-account">
    <h1>Account</h1>

    <p><strong>My account</strong> : {{ $store.state['user'].user.username }}</p>

    <a-space>
      <router-link to="/dashboard/my-account/edit-team">
        <a-button type="primary">Edit team</a-button>
      </router-link>
      <a-button @click="logout()" type="text" danger>Log out</a-button>
    </a-space>

    

  </div>
</template>

<script>
import { authAxios } from '../../utils/auth'

export default {
  mounted() {
    authAxios.get('/api/v1/users/me/')
      .then(response => {
        this.$store.commit('user/setUser', response.data)
        localStorage.setItem('userId', response.data.id)
        localStorage.setItem('userName', response.data.username)
        localStorage.setItem('userEmail', response.data.email)
      })
      .catch(error => {
        console.log(JSON.stringify(error))
      })
  },
  methods: {
    logout() {
      authAxios.post('/api/v1/token/logout/')
        .then(() => {
          localStorage.removeItem('token')
          this.$store.commit('user/removeToken')
          this.$router.push('/')
          localStorage.removeItem('userId')
          localStorage.removeItem('userName')
          localStorage.removeItem('userEmail')
        })
    }
  }
}
</script>
