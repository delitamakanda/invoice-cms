import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import Antd from 'ant-design-vue'
import filters from './helpers/filters'
import { i18n } from './i18n/lang'
import { datadogRum } from '@datadog/browser-rum';

datadogRum.init({
    applicationId: import.meta.VUE_APP_DATADOG_APPLICATION_ID,
    clientToken: import.meta.VUE_APP_DATADOG_CLIENT_TOKEN,
    site: import.meta.VUE_APP_DATADOG_SITE,
    service: import.meta.VUE_APP_DATADOG_SERVICE,
    env: import.meta.VUE_APP_DATADOG_ENV,
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

const pinia = createPinia()

const app = createApp(App)
app.config.globalProperties.$filters = filters
app.use(pinia).use(i18n).use(Antd).use(store).use(router, axios).mount('#app')
