import axios from 'axios'
import Cookies from 'js-cookie'

export default {
  state: {
    accessToken: null,
    userLoaded: false
  },
  getters: {
    loggedIn(state) {
      return state.accessToken == null ? false : true
    }
  },
  mutations: {
    updateToken(state, token) {
      state.accessToken = token
      state.userLoaded = true
    },
    deleteToken(state) {
      state.accessToken = null
      state.userLoaded = true
    }
  },
  actions: {
    login: ({ commit }, payload) => {
      return new Promise((resolve, reject) => {
        axios.post('/api/auth/token', payload)
        .then(({ data, status }) => {
          if (status === 200) {
            commit('updateToken', data.access)
            resolve(true)
          }
        })
        .catch(error => {
          reject(error)
        });
      });
    },
    logout: ({ commit }, payload) => {
      commit('deleteToken')
      
      // if (payload) {
        axios.post('/api/auth/logout')
        .catch(error => {
          return error
        })
      // }
    },
    register: ({ commit }, payload) => {
      return new Promise((resolve, reject) => {
        axios.post('/api/auth/register', payload)
        .then(({ data, status }) => {
          if (status === 201) {
            resolve(true);
          }
        })
        .catch(error => {
          reject(error)
        });
      });
    },
    refreshToken: ({ commit }, payload) => {
      return new Promise((resolve, reject) => {
        axios.post('/api/auth/token/refresh')
        .then(response => {
          commit('updateToken', response.data.access)
          resolve(true)
        })
        .catch(error => {
          reject(error)
        })
      })
    }
  }
};