<template>
  <div class="h-full mb-20 sm:mb-0">
    <div class="relative top-1/2 transform -translate-y-1/2 max-w-md mx-auto p-8">
      <FormFields 
        title="Register"
        :fieldsConfig="{
          firstname: 'text',
          lastname: 'text',
          email: 'email',
          password: 'password'
        }"
        :action="action"
        @success="registerSuccess"
      />
      <div class="flex justify-end">
        <router-link :to="{path: '/login', query: {redirect: $route.query.redirect}}" class="gray-900 hover:underline">Have Account?</router-link>
      </div> 
    </div>
  </div>
</template>

<script>
import FormFields from '@/components/FormFields.vue'

export default {
  components: {
    FormFields
  },
  computed: {
    action() {
      return this.$route.query.redirect === 'checkout' ? 'register#' : 'register'
    }
  },
  methods: { 
    registerSuccess() {
      if (this.$route.query.redirect === 'checkout') {
        alert('Successfully registered. Please log in to continue to checkout.')
      }
      else
        alert('Successfully registered. You may need to login.')
      this.$router.push('/login')
    }
  }
}
</script>