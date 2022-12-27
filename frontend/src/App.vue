<template>
  <a-layout has-sider>
    <a-layout-sider
      id="components-layout-demo-fixed-sider" 
      :style="{ overflow: 'auto', height: '100vh', position: 'fixed', background: '#fff', left: 0, top: 0, bottom: 0}"
    >
      <div class="logo" />
      <a-menu v-model:selectedKeys="selectedKeys" v-model:openKeys="openKeys" mode="inline">
        <a-sub-menu key="sub1" v-if="store.state['user'].isLoggedIn">
          <template #title>
              <span>
                <home-outlined />                
                Dashboard
              </span>
          </template>
            <a-menu-item key="1">
            <video-camera-outlined />
            <span class="nav-text"><router-link to="/">Home</router-link></span>
          </a-menu-item>
          <a-sub-menu key="sub3" title="Clients">
            <a-menu-item key="2">
              <bar-chart-outlined />
              <span class="nav-text"><router-link to="/dashboard/clients">Clients</router-link></span>
            </a-menu-item>
            <a-menu-item key="3">
              <usergroup-add-outlined />
              <span class="nav-text"><router-link to="/dashboard/clients/add">Add client</router-link></span>
            </a-menu-item>
        </a-sub-menu>
        <a-sub-menu key="sub4" title="Invoices">
            <a-menu-item key="4">
              <bar-chart-outlined />
              <span class="nav-text"><router-link to="/dashboard/invoices">Invoices</router-link></span>
            </a-menu-item>
            <a-menu-item key="5">
              <upload-outlined />
              <span class="nav-text"><router-link to="/dashboard/invoices/add">Add invoice</router-link></span>
            </a-menu-item>
          </a-sub-menu>
          <a-sub-menu key="sub2" title="My account">
            <a-menu-item key="6">
              <user-outlined />
              <span class="nav-text"><router-link to="/dashboard/my-account">User info</router-link></span>
            </a-menu-item>
            <a-menu-item key="7">
              <bar-chart-outlined />
              <span class="nav-text"><router-link to="/dashboard/my-account/edit-team">Edit team</router-link></span>
            </a-menu-item>
            <a-menu-item key="8">
              <logout-outlined />
              <span class="nav-text" @click="logout()">Logout</span>
            </a-menu-item>
          </a-sub-menu>
        </a-sub-menu>
        <template v-if="!store.state['user'].isLoggedIn">
          <a-menu-item key="1">
            <user-add-outlined />
            <span class="nav-text"><router-link to="/sign-up">Sign up</router-link></span>
          </a-menu-item>
          <a-menu-item key="2">
            <login-outlined />
            <span class="nav-text"><router-link to="/sign-in">Log in</router-link></span>
          </a-menu-item>
        </template>
        <a-menu-item :key="store.state['user'].isLoggedIn ? '9' : '3'">
          <tool-outlined />
          <span class="nav-text"><router-link to="/about">About</router-link></span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout :style="{ marginLeft: '200px' }">
      <a-layout-header :style="{ background: '#fff', padding: 0 }" />
      <a-layout-content :style="{ margin: '24px 16px 0', overflow: 'initial' }">
        <div :style="{ padding: '24px', background: '#fff', minHeight: '280px' }">
          <router-view />
        </div>
      </a-layout-content>
      <a-layout-footer :style="{ textAlign: 'center' }">
        {{title}} ©{{fullYear}}
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>

<script>
  import { authAxios } from './utils/auth'
  import { defineComponent, reactive, toRefs } from 'vue'
  import { title } from './utils/constants'
  import { useStore } from 'vuex'
  import { useRouter } from 'vue-router'
  import { UserOutlined, VideoCameraOutlined, UploadOutlined, BarChartOutlined, CloudOutlined, AppstoreOutlined, TeamOutlined, ShopOutlined, HomeOutlined, LoginOutlined, LogoutOutlined, UserAddOutlined, UsergroupAddOutlined, ToolOutlined } from '@ant-design/icons-vue'

  export default defineComponent({
    components: {
      UserOutlined,
      VideoCameraOutlined,
      UploadOutlined,
      BarChartOutlined,
      CloudOutlined,
      AppstoreOutlined,
      TeamOutlined,
      ShopOutlined,
      HomeOutlined,
      LoginOutlined,
      LogoutOutlined,
      UserAddOutlined,
      UsergroupAddOutlined,
      ToolOutlined,
    },
    setup() {
      const store = useStore()
      const router = useRouter()

      store.commit('user/initStore')

      const state = reactive({
        mode: 'inline',
        theme: 'light',
        selectedKeys: ['2'],
        openKeys: ['sub1'],
        collapsed: false,
      })

      const logout = () => {
        authAxios.post('/api/v1/token/logout/')
        .then(() => {
          localStorage.removeItem('token')
          store.commit('user/removeToken')
          router.push('/sign-in')
          localStorage.removeItem('userId')
          localStorage.removeItem('userName')
          localStorage.removeItem('userEmail')
        })
      }
      
      return {
        ...toRefs(state),
        title,
        fullYear: new Date().getFullYear(),
        store,
        logout,
        router,
      }
    },
  })
</script>

<style lang="scss">
#components-layout-demo-fixed-sider .logo {
  height: 32px;
  background: rgba(0, 0, 0, 0.2);
  margin: 16px;
}
.site-layout .site-layout-background {
  background: #fff;
}

[data-theme='dark'] .site-layout .site-layout-background {
  background: #141414;
}
</style>