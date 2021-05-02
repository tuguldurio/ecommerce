import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './assets/tailwind.css'
import axios from 'axios'

axios.defaults.baseURL = 'http://192.168.0.235:8000'
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.withCredentials = true

axios.interceptors.request.use(
  function(config) {
    // store
    const token = store.state.user.accessToken;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  function(error) {
    // Do something with request error
    return Promise.reject(error)
  }
)

let isAlreadyFetchingAccessToken = false
let subscribers = []

function onAccessTokenFetched(access_token) {
  subscribers = subscribers.filter(callback => callback(access_token))
}

function addSubscriber(callback) {
  subscribers.push(callback)
}

axios.interceptors.response.use(
  response => {
    return response;
  },
  async error => {
    if (error.response.status === 404) {
      store.dispatch('error404')
    }
    /* refresh token and retry request once more on 401
       else log user out
    */
    const {config: originalReq, response} = error

    // skip refresh token request, retry attempts to avoid infinite loops
    if (originalReq.url !== '/api/auth/token/refresh' && !originalReq.isRetryAttempt && response && response.status === 401) {
      try {
        await store.dispatch('refreshToken')
        originalReq.isRetryAttempt = true
        // originalReq.headers['Authorization'] = request.defaults.headers.common['Authorization']
        return await axios(originalReq)
      } catch (e) {
        // log user out if fail to refresh (due to expired or missing token) or persistent 401 errors from original requests
        if (e.response && e.response.status === 401) {
          store.dispatch('logout', true)
        }
        // suppress original error to throw the new one to get new information
        // throw e
        throw error
      }
    } else {
      throw error
    }
  }
)

// router.beforeEach((to, from, next) => {
//   store.dispatch('resetError404')
//   next()
// })

router.afterEach((to, from) => {
  store.dispatch('resetError404')
})

createApp(App).use(store).use(router).mount('#app')