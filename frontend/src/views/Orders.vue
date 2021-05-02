<template>
  <div class="container mx-auto">
    <div v-for="order in orders" :key="order.id">
      {{order}}
    </div>
  </div>  
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      orders: ''
    }
  },
  methods: {
    async fetchProduct() {
      try {
        const response = await axios.get('/api/orders')
        this.orders = response.data
      } catch (error) {
        console.log(error.response)
      }
    }
  },
  created() {
    this.fetchProduct()
  }
}
</script>