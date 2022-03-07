export const namespaced = true

export const state = {
    user: {
        username: ''
    },
    isLoggedIn: false,
    token: ''
}

export const getters = {}

export const mutations = {
    initStore(state) {
        if (localStorage.getItem('token')) {
            state.token = localStorage.getItem('token')
            state.isLoggedIn = true
        } else {
            state.token = ''
            state.isLoggedIn = false
        }
    },
    setToken(state, token) {
        state.token = token
        state.isLoggedIn = true
    },
    removeToken(state) {
        state.token = ''
        state.isLoggedIn = false
    }
}

export const actions = {}

export const modules = {}