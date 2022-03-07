import axios from 'axios'

import { endpoint } from './constants'

export const authAxios = axios.create({
    baseURL: endpoint,
    timeout: 1000
})


authAxios.interceptors.request.use(function(config) {
    config.headers['Authorization'] = `Token ${localStorage.getItem('token')}`;
    config.headers['Content-Type'] = 'application/json';

    return config
}, function(error) {
    return Promise.reject(error)
})
