<template>
  <div v-if="loaded"
    class="w-full sm:w-11/12 xl:w-5/6 2xl:w-3/5 flex flex-wrap lg:flex-nowrap lg:flex-row mx-auto mb-8 sm:my-8"   
  >
    <!-- if cart has prodcuts -->
    <template v-if="hasItems">
      <div class="w-full lg:w-2/3 xl:w-2/3 flex flex-col space-y-4 p-8 lg:mr-3 bg-white rounded shadow-lg">
        <div class="hidden sm:flex flex-row text-center">
          <div class="w-1/4 font-semibold"></div>
          <div class="w-1/4 font-semibold">Product details</div>
          <div class="w-1/4 font-semibold">Quantity</div>
          <div class="w-1/4 font-semibold">Total price</div>
        </div>

        <div class="flex flex-row sm:text-center" 
          v-for="product in cartProducts" :key="product.id"
        >
          <img class="w-1/3 h-full object-cover sm:w-1/4 rounded" :src="product.image" alt="">
          <div class="w-2/3 h-full sm:w-3/4 mt-0 flex flex-col sm:flex-row items-center">
            <div class="w-full sm:w-1/3 px-5">
              <p class="text-lg font-semibold">{{product.name}}</p>
              <p class="font-medium">${{convertPrice(product.unit_price)}}</p>
            </div>
            <div class="relative w-full sm:w-1/3">
              <Quantity class="w-28 h-6 mx-5 sm:mx-auto" :quantity="product.quantity"  @update="updateQuantity(product, $event)"/>
              <button class="sm:absolute sm:left-1/2 sm:transform sm:-translate-x-1/2 mx-5 sm:mx-0 text-sm hover:underline" @click="deleteProduct(product)">Remove</button>
            </div>
            <p class="w-full sm:w-1/3 px-5 sm:mx-auto font-semibold">${{convertPrice(product.unit_price*product.quantity).toFixed(2)}}</p>
          </div>
        </div>
      </div>
      
      <div class="sticky top-20 w-full lg:w-1/3 xl:w-1/3 h-full lg:ml-3 p-4 sm:p-8 rounded shadow-lg">
        <div class="lg:px-4 lg:py-2 m-2 text-lg lg:text-xl font-semibold text-center">Subtotal: ${{totalPrice}}</div>
        <Button class="w-full py-3 uppercase font-medium" @click="gotoCheckout">{{checkout}}</Button>
      </div>
    </template>

    <!-- if there is no items in cart -->
    <div v-else class="mx-auto text-2xl">
      No items in the cart
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Cookies from 'js-cookie'

import Button from '@/components/Button.vue'
import Quantity from '@/components/Cart/Quantity.vue'

export default {
  components: {
    Button,
    Quantity
  },
  data() {
    return {
      cartProducts: [],
      checkout: 'checkout',
      loaded: false,
      error: null,
    }
  },
  mounted() {
    if (this.loggedIn) {
      this.fetchProducts()
    }
    else {
      this.fetchProductsFromCookie()
    }
  },
  computed: {
    hasItems() {
      return this.cartProducts.length > 0 ? true : false
    },
    totalPrice() {
      let total = 0

      this.cartProducts.forEach(product => {
        total += product.unit_price * product.quantity
      })
      return this.convertPrice(total)
    },
    loggedIn() {
      return this.$store.getters.loggedIn
    }
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await axios.get('/api/cart')
        this.cartProducts = response.data
        this.loaded = true
      } catch (error) {
        this.error = error.response.detail
      }
    },
    async fetchProductsFromCookie() {
      const cartCookie = Cookies.get('cart')
      if (cartCookie) {
        const cartProducts = []
        const cart = JSON.parse(cartCookie)

        for (let i = 0; i < cart.length; i++) {
          const response = await axios.get(`/api/products/${cart[i].id}`)
          const data = response.data
          cartProducts.push({
            'id': cart[i].id,
            'name': data.name,
            'image': data.images[0],
            'unit_price': data.price,
            'quantity': cart[i].quantity,
          })
        }
        this.cartProducts = cartProducts
      }
      this.loaded = true
    },
    /** updates cart products */
    async updateQuantity(product, quantity) {
      if (this.loggedIn) {
        try {
          await axios.put(`api/cart/products/${product.id}`, {quantity: quantity})
        } catch (error) {
          console.log(error.response)
          alert(error.response.data)
        } finally {
          this.fetchProducts()
        }
      }
      else {
        const cartCookie = Cookies.get('cart')
        if (cartCookie) {
          let cart = JSON.parse(cartCookie)

          cart.forEach(e => {
            if (e.id === product.id) {
              e.quantity = quantity
            }
          })

          Cookies.set('cart', JSON.stringify(cart), { expires: 7 })
        }
        this.fetchProductsFromCookie()
      }
    },
    /** deletes product from cart */
    async deleteProduct(product) {
      if (this.loggedIn) {
        try {
          const response = await axios.delete('/api/cart/products/'+product.id)
        } catch (error) {
          this.error = error.response.detail
        }
        this.fetchProducts()
      }
      else {
        const cartCookie = Cookies.get('cart')
        if (cartCookie) {
          let cart = JSON.parse(cartCookie)
          cart = cart.filter(e => e.id !== product.id)
          Cookies.set('cart', JSON.stringify(cart), { expires: 7 })
        }
        this.fetchProductsFromCookie()
      }
    },
    gotoCheckout() {
      if (this.loggedIn) {
        this.$router.push('/checkout')
      }
      else {
        this.$router.push({path: '/login', query: {redirect: 'checkout'}})
      }
    },
    convertPrice(price) {
      return price / 100
    }
  }
}
</script>