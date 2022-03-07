<template>
  <div class="page-account">
    <h1>Account</h1>

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
