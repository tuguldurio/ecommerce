<template>
  <Navbar @openCart="showCart=true"/>
  
  <main class="pt-16 flex-1">
    <Error404 v-if="error404"/>
    <router-view v-else/>
  </main>

  <Footer/>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import Error404 from '@/views/error/404.vue'

export default {
  name: 'App',
  components: {
    Navbar,
    Footer,
    Error404
  },
  computed: {
    loggedIn() {
      return this.$store.getters.loggedIn
    },
    error404() {
      return this.$store.state.error.error404
    }
  },
  beforeCreate() {
    this.$store.dispatch('refreshToken')
  }
}
</script>

<style lang="scss">
html, body {
  height: 100%;
}

@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&display=swap');
</style>