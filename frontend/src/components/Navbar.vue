<template>
  <nav class="fixed top-0 z-30 inset-x-0 bg-black text-white h-16">
    <div class="container mx-auto h-full flex items-center justify-between">
      <div class="w-auto">
        <a href="/" class="text-3xl font-semibold mr-8 cursor-pointer">Ecommerce</a>
      </div>

      <div class="flex flex-row w-auto h-full items-center">
        <div class="flex items-center h-full space-x-4 mr-8">
          <router-link class="text-xl font-medium hover:underline" to="/shop">Shop</router-link>
          <router-link class="text-xl font-medium hover:underline" to="/about">About</router-link>
          <router-link class="text-xl font-medium hover:underline" to="/contact">Contact</router-link>
        </div>

        <div class="mr-2 relative mx-auto text-black">
          <input class=" bg-white px-5 py-2 pr-10 rounded-none focus:outline-none"
            type="search" name="search" placeholder="Search">
          <button type="submit" class="absolute right-0 top-0 p-2 focus:outline-none">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </button>
        </div>

        <div class="relative flex items-center mr-1 py-4 px-1 cursor-pointer" @click="showUser=!showUser" @mouseover="showUser=true" @mouseleave="showUser=false" >
          <svg class="w-8" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          
          <div v-if="showUser" class="absolute top-15 -right-0 w-44 bg-white text-black text-base z-30 float-left py-2 list-none shadow-lg mt-1">
            <template v-if="loggedIn">
              <a class="py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent hover:underline cursor-pointer" 
                @click="gotoOrders"
              >
                Orders
              </a>
              <a class="py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent hover:underline cursor-pointer">
                Settings
              </a>
              <a class="py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent hover:underline cursor-pointer"
               @click="logout"
              >
                Log out
              </a>
            </template>
            <template v-else>
              <a class="py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent hover:underline cursor-pointer"
                @click="login"
              >
                Log in
              </a>
              <a @click="register" class="py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent hover:underline cursor-pointer">
                Register
              </a>
            </template>
          </div>
        </div>
        
        <div class="flex items-center mr-1 py-2">
          <svg class="w-8 cursor-pointer" @click="gotoCart" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
          </svg>
        </div>

      </div>
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      showUser: false
    }
  },
  computed: {
    userLoaded() {
      return this.$store.state.user.userLoaded
    },
    loggedIn() {
      return this.$store.getters.loggedIn
    }
  },
  methods: {
    gotoHome() {
      if (this.$route.path !== '/') {
        this.$router.push('/')
      }

      window.scroll({
        top: 0,
        left: 0,
        behavior: 'smooth'
      })
    },
    logout() {
      this.$router.push('/')
      this.$store.dispatch('logout')
    },
    login() {
      this.$router.push('/login')
    },
    register() {
      this.$router.push('/register')
    },
    gotoOrders() {
      this.$router.push('/orders')
    },
    gotoCart() {
      this.$router.push('/cart')
    },
  }
}
</script>