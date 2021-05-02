<template>
  <div class="h-full mb-20 sm:mb-0">
    <div class="relative top-1/2 transform -translate-y-1/2 max-w-md mx-auto p-8">
      <FormFields 
        title="Login"
        :fieldsConfig="{
          email: 'email',
          password: 'password'
        }"
        action="login"
        @success="loginSuccess"
        @error="loginError"
      />
      <div class="flex justify-end">
        <router-link :to="{path: '/register', query: {redirect: $route.query.redirect}}" class="hover:underline">Create account</router-link>
      </div> 
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Cookies from 'js-cookie'
import FormFields from '@/components/FormFields.vue'

export default {
  components: {
    FormFields
  },
  methods: {
    loginSuccess() {
      if (this.$route.query.redirect === 'checkout') {
        const cartCookie = Cookies.get('cart')
        if (cartCookie) {
          const cart = JSON.parse(cartCookie).map(e => {
            return { product_id: e.id, quantity: e.quantity }
          })
          axios.post('/api/cart', cart)
          this.$router.push({name: this.$route.query.redirect})
        }
      }
      else this.$router.push('/')
    },
    loginError(error) {
      console.log(error.response)
    }
  }
}
</script>