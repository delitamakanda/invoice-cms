export const namespaced = true

export const state = {
    user: {
        id: '',
        username: '',
        email: ''
    },
    isLoggedIn: false,
    token: ''
}

export const getters = {
    user: state => state.user
}

export const mutations = {
    initStore(state) {
        if (localStorage.getItem('token')) {
            state.token = localStorage.getItem('token')
            state.isLoggedIn = true
            state.user.id = localStorage.getItem('userId')
            state.user.username = localStorage.getItem('userName')
            state.user.email = localStorage.getItem('userEmail')
        } else {
            state.user.id = ''
            state.user.username = ''
            state.user.email = ''
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
        state.user.id = ''
        state.user.username = ''
        state.user.email = ''
    },
    setUser(state, user) {
        state.user = user
    }
}

export const actions = {}
