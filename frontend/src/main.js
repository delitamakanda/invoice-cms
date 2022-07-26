import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import Antd from 'ant-design-vue'
import filters from './helpers/filters'
import 'ant-design-vue/dist/antd.css'

axios.defaults.baseURL = '/'

const app = createApp(App)
app.config.globalProperties.$filters = filters
app.use(Antd).use(store).use(router, axios).mount('#app')
