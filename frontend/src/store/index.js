import { createStore } from 'vuex'

import * as user from './user'

const store = createStore({
  strict: true,
  modules: {
    user
  }
})

export default store