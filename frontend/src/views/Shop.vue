<template>
  <div class="container mx-auto mt-16">
    <p class="mb-4 text-3xl text-center">All Products</p>
    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-0 md:gap-10">
      <div class="flex flex-col items-center h-96"
        v-for="product in products" :key="product.id"
      >
        <router-link class="h-4/5" :to="`/products/${product.id}`">
          <img class="h-full object-cover mx-auto cursor-pointer" 
            :src="product.images[0]" alt="image"
          >
        </router-link>
        <div class="h-1/5">
          <p class="text-xl text-center">{{ product.name }}</p>
          <p class="text-lg text-center">${{ product.price/100 }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      products: [] 
    }
  },
  mounted() {
    this.fetchProducts()
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await axios.get('/api/products/all')
        this.products = response.data
      } catch (error) {
        console.log(error)
      }
    }
  }
}
</script>

<style>

</style>