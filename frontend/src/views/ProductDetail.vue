<template>
  <div class="w-full sm:w-3/4 lg:w-2/3 mx-auto my-8 sm:my-16">
    <div class="flex flex-wrap">

      <swiper navigation pagination class="w-full md:w-1/2">
        <swiper-slide v-for="(image, index) in images" :key="index">
          <img :src="image" alt="" class="w-full h-128 object-scale-down object-top">
        </swiper-slide>
      </swiper>

      <div class="w-full md:w-1/2">
        <div class="w-10/12 mx-auto">
          <p class="text-3xl font-semibold">{{name}}</p>
          <p class="text-2xl font-sans mt-2">${{price/100}}</p>

          <div class="w-full sm:w-1/2 flex flex-col mt-4">
            <Quantity class="h-10" :quantity="quantity" @update="updateQuantity" />
            <Button class="h-12 mt-2 font-medium" @click="addToCart">{{buttonValue}}</Button>
          </div>
        </div>
      </div>
    </div>

    <CartModal ref="cart-modal" :quantity="quantity"/>
  </div>
</template>

<script>
import axios from 'axios'
import Cookies from 'js-cookie'

import { Swiper, SwiperSlide } from 'swiper/vue';
import SwiperCore, { Navigation, Pagination, Scrollbar, A11y } from 'swiper';
import 'swiper/swiper.scss';
import 'swiper/components/navigation/navigation.scss';
import 'swiper/components/pagination/pagination.scss';
import 'swiper/components/scrollbar/scrollbar.scss';

import Button from '@/components/Button.vue'
import Quantity from '@/components/Cart/Quantity.vue'
import CartModal from '@/components/Cart/Modal.vue'

SwiperCore.use([Navigation, Pagination, Scrollbar, A11y]);

export default {
  components: {
    Button,
    Quantity,
    CartModal,

    Swiper,
    SwiperSlide,
  },
  data() {
    return {
      productId: '',
      name: '',
      images: [],
      price: [],
      quantity: 1,
      buttonValue: 'Add to cart'
    }
  },
  computed: {
    loggedIn() {
      return this.$store.getters.loggedIn
    }
  },
  methods: {
    async fetchProducts() {
      try {
        const {data} = await axios.get(`/api/products/${this.$route.params.id}`)
        this.productId = data.id
        this.name = data.name
        this.images = data.images
        this.price = data.price
      } catch (error) {
        console.log(error.response)
      }
    },
    async addToCart() {
      this.buttonValue = 'Adding to cart...'
      if (this.loggedIn) {
        try {
          const response = await axios.post(`/api/cart/products/${this.productId}`, {quantity: this.quantity})
          this.$refs['cart-modal'].show()
        } catch (error) {
          alert(error.response.data)
        } finally {
          this.buttonValue = 'Add to cart'
        }
      }
      /** Save cart information to cookies when not logged in */
      else {
        const info = {'id': this.productId, 'quantity': this.quantity}

        const cartCookie = Cookies.get('cart')
        if (cartCookie) {
          const cart = JSON.parse(cartCookie)
          let exists = false

          cart.forEach(e => {
            if (e.id == this.productId) {
              e.quantity += this.quantity
              exists = true
            }
          })
          if (!exists)
            cart.push(info)

          Cookies.set('cart', JSON.stringify(cart), { expires: 7 })
          this.$refs['cart-modal'].show()
        }
        else {
          const cart = [info]
          Cookies.set('cart', JSON.stringify(cart), { expires: 7 })
        }
        this.buttonValue = 'Add to cart'
      }
    },
    updateQuantity(quantity) {
      this.quantity = quantity
    },
  },
  created() {
    this.fetchProducts()
  }
}
</script>