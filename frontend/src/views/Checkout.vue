<template>
  <div wire:loading class="fixed top-0 left-0 right-0 bottom-0 w-full h-screen z-50 overflow-hidden bg-gray-700 opacity-75 flex flex-col items-center justify-center">
    <div class="loader ease-linear rounded-full border-4 border-t-4 border-gray-200 h-12 w-12 mb-4"></div>
    <h2 class="text-center text-white text-xl font-semibold">Loading...</h2>
    <p class="w-1/3 text-center text-white">This may take a few seconds, please don't close this page.</p>
  </div>
</template>

<script>
import axios from 'axios'
import { loadStripe } from '@stripe/stripe-js';

let attempts = 0

export default {
  methods: {
    checkAvailibility() {

    },
    async createSession() {
      attempts += 1
      try {
        const response = await axios.post('/api/order/create-checkout-session')
        const stripe = await loadStripe(response.data.publicKey)
        const result = await stripe.redirectToCheckout({sessionId: response.data.sessionId});
        if (result.error) {
          alert(result.error.message);
        }
      } catch (error) {
        if (attempts >= 3) {
          alert('Error occured while trying to redirect to checkout')
          this.$router.push('/cart')
          return
        }
        this.createSession()
      }
    },
  },
  created() {
    this.checkAvailibility()
    this.createSession()
  }
}
</script>

<style>
.loader {
	border-top-color: #3498db;
	-webkit-animation: spinner 1.5s linear infinite;
	animation: spinner 1.5s linear infinite;
}

@-webkit-keyframes spinner {
	0% {
		-webkit-transform: rotate(0deg);
	}
	100% {
		-webkit-transform: rotate(360deg);
	}
}

@keyframes spinner {
	0% {
		transform: rotate(0deg);
	}
	100% {
		transform: rotate(360deg);
	}
}
</style>