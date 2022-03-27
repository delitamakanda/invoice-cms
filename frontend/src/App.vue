<template>
  <a-layout class="layout">
    <a-layout-header>
      <a-menu theme="dark" mode="horizontal" v-model:selectedKeys="selectedKeys" :style="{ lineHeight: '64px' }">
        <a-menu-item key="1"><router-link to="/">Dashboard - {{title}}</router-link></a-menu-item>
        <template v-if="store.state['user'].isLoggedIn">
          <a-menu-item key="2"><router-link to="/dashboard/clients">Clients</router-link></a-menu-item>
          <a-menu-item key="3"><router-link to="/dashboard/invoices">Invoices</router-link></a-menu-item>
          <a-menu-item key="4"><router-link to="/dashboard/my-account">My account</router-link></a-menu-item>
        </template>
        <template v-else>
          <a-menu-item key="2"><router-link to="/sign-up">Sign up</router-link></a-menu-item>
          <a-menu-item key="3"><router-link to="/sign-in">Log in</router-link></a-menu-item>
        </template>
        <a-menu-item :key="!store.state['user'].isLoggedIn ? '4' : '5'"><router-link to="/about">About</router-link></a-menu-item>
      </a-menu>
    </a-layout-header>
    <a-layout-content style="padding: 0 50px">
      <div :style="{ background: '#fff', margin: '16px 0', padding: '24px', minHeight: '280px' }">
        <router-view />
      </div>
    </a-layout-content>
    <a-layout-footer style="text-align: center">
      {{title}} ©{{fullYear}}
    </a-layout-footer>
  </a-layout>
</template>

<script>
  import { defineComponent, ref } from 'vue'
  import { title } from './utils/constants'
  import { useStore } from 'vuex'

  export default defineComponent({
    setup() {
      const store = useStore()

      store.commit('user/initStore')
      
      return {
        selectedKeys: ref(['1']),
        title,
        fullYear: new Date().getFullYear(),
        store
      
      }
    },
  })
</script>

<style lang="scss">
.site-layout-content {
  min-height: 280px;
  padding: 24px;
  background: #fff;
}
#components-layout-demo-top .logo {
  float: left;
  width: 120px;
  height: 31px;
  margin: 16px 24px 16px 0;
  background: rgba(255, 255, 255, 0.3);
}
.ant-row-rtl #components-layout-demo-top .logo {
  float: right;
  margin: 16px 0 16px 24px;
}

[data-theme='dark'] .site-layout-content {
  background: #141414;
}
</style>