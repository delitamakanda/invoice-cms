<template>
  <div class="page-account">
    <h1>Account</h1>

    <a-button @click="logout()" type="primary">Log out</a-button>

  </div>
</template>

<script>
import { authAxios } from '../../utils/auth'

export default {
  methods: {
    logout() {
      authAxios.post('/api/v1/token/logout/')
        .then(response => {
          localStorage.removeItem('token')
          this.$store.commit('user/removeToken')
          this.$router.push('/')
        })
    }
  }
}
</script>
