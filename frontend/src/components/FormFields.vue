<template>
  <form class=""
    @submit.prevent="handleSubmit"
  >
    <h4 class="mb-2 text-center text-2xl">{{title}}</h4>

    <div v-if="!Object.values(errors).every(x => (x === null))" class="p-2 text-center bg-red-100 text-red-600 border border-red-400 rounded">
      <template v-for="(value, key) in errors" :key="key">
        <div v-if="errors[key]">
        * {{value}}
        </div>
      </template>
    </div>

    <div v-for="(value, key) in fields" :key="key">
      <input v-model="fields[key]" :type="fieldsConfig[key]" :placeholder="key" class="w-full mt-2 py-2 px-3 appearance-none border-b border-black rounded-none outline-none"
      :class="errors[key] ? 'bg-red-100 border-red-400 focus:border-red-800' : ''">
    </div>

    <!-- <button class="mt-2 w-full bg-gray-900 text-white p-2 rounded" @submit.prevent="handleSubmit">Submit</button> -->
    <Button class="w-full mt-2 " @submit.prevent="handleSubmit">Submit</Button>
  </form>
</template>

<script>
import Cookies from 'js-cookie'
import Button from '@/components/Button.vue'

export default {
  components: {
    Button
  },
  props: {
    title: String,
    fieldsConfig: Object,
    action: String
  },
  data() {
    return {
      fields: {},
      errors: {}
    }
  },
  methods: {
    handleSubmit() {
      let payload = this.fields

      if (this.action === 'register#') {
        const cartCookie = Cookies.get('cart')
        if (cartCookie) {
          const cart = JSON.parse(cartCookie).map(e => {
            return { product_id: e.id, quantity: e.quantity }
          })
          payload.products = cart
        }
      }

      this.$store.dispatch(this.action.replace('#', ''), payload)
      .then(() => {
        this.$emit('success')
      })
      .catch(error => {
        if (error.response.status === 400 && error.response.statusText === 'Bad Request') {
          let errorData = error.response.data
          for (const [name, type] of Object.entries(errorData)) {
            this.errors[name] = type[0]
          }
        } 
        else {
          this.errors.generic = error.response.data.detail
        }
        this.$emit('error', error)
      })
    }
  },
  created() {
    this.errors.generic = null
    for (const [name, type] of Object.entries(this.fieldsConfig)) {
      this.fields[name] = ''
      this.errors[name] = null
    }
  }
}
</script>