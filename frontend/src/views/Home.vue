<template>
  <div class="">
    <div class="relative overflow-hidden h-128">
      <img class="absolute w-full h-full object-cover object-center-hero" src="@/assets/theo-sautif-zoTPkqGfZi0-unsplash.jpg" alt="">

      <div class="relative h-full w-full bg-gray-900 bg-opacity-30">
        <div class="absolute top-1/2 left-40 right-1/2 inset-x-2.5">
          <div>
            <h1 class="text-white text-3xl md:text-6xl">Your desired products</h1>
            <Button class="mt-3 py-3" color="white" :border="false" @click="$router.push('/shop')">Start Shopping</Button>
          </div>
        </div>
      </div>
    </div>

    <div class="container mx-auto">
      <FdProducts/>
    </div>
  </div>
</template>

<script>
import Button from '@/components/Button.vue'
import FdProducts from '@/components/FeaturedProducts.vue'

export default {
  name: 'Home',
  components: {
    Button,
    FdProducts
  },
}
</script>
