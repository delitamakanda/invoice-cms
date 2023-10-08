require('dotenv').config()

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import Antd from 'ant-design-vue'
import filters from './helpers/filters'
import { i18n } from './i18n/lang'
import 'ant-design-vue/dist/antd.css'
import { datadogRum } from '@datadog/browser-rum';

datadogRum.init({
    applicationId: process.env.VUE_APP_DATADOG_APPLICATION_ID,
    clientToken: process.env.VUE_APP_DATADOG_CLIENT_TOKEN,
    site: process.env.VUE_APP_DATADOG_SITE,
    service: process.env.VUE_APP_DATADOG_SERVICE,
    env: process.env.VUE_APP_DATADOG_ENV,
    // Specify a version number to identify the deployed version of your application in Datadog 
    // version: '1.0.0', 
    sessionSampleRate:100,
    sessionReplaySampleRate: 20,
    trackUserInteractions: true,
    trackResources: true,
    trackLongTasks: true,
    defaultPrivacyLevel:'mask-user-input'
});
    
datadogRum.startSessionReplayRecording();

axios.defaults.baseURL = '/'

const app = createApp(App)
app.config.globalProperties.$filters = filters
app.use(i18n).use(Antd).use(store).use(router, axios).mount('#app')
