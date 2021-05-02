<template>
  <div class="flex h-8 border border-black">
    <button 
    class="w-12 px-1 bg-white"
    @click="decrease"
    >
      <svg class="w-full" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M20 12H4"/>
      </svg>
    </button>

    <input class="w-full text-xl text-center"
      ref="quantity"
      type="text" min="0" :value="quantity" @change="changed"
    >

    <button 
    class="w-12 px-1 bg-white"
    @click="increase"
    >
      <svg class="w-full" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
      </svg>
    </button>
  </div>
</template>

<script>
export default {
  props: {
    quantity: Number
  },
  methods: {
    decrease() {
      if (this.quantity > 1) {
        this.$emit('update', parseInt(this.$refs.quantity.value)-1)
      }
    },
    increase() {
      this.$emit('update', parseInt(this.$refs.quantity.value)+1)
    },
    changed(event) {
      this.$emit('update', parseInt(this.$refs.quantity.value))
    },
  },
  // watch: {
  //   quantity(newQuantity, oldQuantity) {
  //     this.$emit('update', newQuantity, oldQuantity)
  //   }
  // }
}
</script>