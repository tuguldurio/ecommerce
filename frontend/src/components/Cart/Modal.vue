<template>
  <div v-if="showModal">
    <BaseModal @close="close"/>

    <div class="absolute w-full lg:max-w-3xl h-auto top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-40 bg-white">
      <svg class="absolute right-0 w-6 m-1 cursor-pointer text-gray-400 hover:text-gray-600" @click="close" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
      </svg>
      <h1 class="px-8 py-4 text-center text-2xl">{{quantity}} items were added to your cart. What's next?</h1>
      <div class="p-6 flex flex-col space-y-3">
        <Button @click="gotoCheckout">Proceed to checkout</Button>
        <Button @click="close">Continue shopping</Button>
        <Button @click="gotoCart">View or edit cart</Button>
      </div>
    </div>
  </div>
</template>

<script>
import Button from '@/components/Button.vue'
import BaseModal from '@/components/BaseModal.vue'

export default {
  components: {
    Button,
    BaseModal
  },
  props: {
    quantity: Number
  },
  data() {
    return {
      showModal: false
    }
  },
  methods: {
    show() {
      this.showModal = true
    },
    close() {
      this.showModal = false
    },
    gotoCheckout() {
      this.$router.replace('/checkout')
    },
    gotoCart() {
      this.$router.push('/cart')
    }
  }
}
</script>