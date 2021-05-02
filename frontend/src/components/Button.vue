<template>
  <button class="px-4 py-2 block item-center rounded-none focus:outline-none"
    :class="classObject"
    :disabled="this.disabled"
  >
    <slot></slot>
  </button>
</template>

<script>
export default {
  props: {
    color: {
      type: String,
      default: 'black'
    },
    disabled: {
      type: Boolean,
      default: false
    },
    border: {
      type: Boolean,
      default: true
    }
  },
  computed: {
    classObject() {
      return {
        'text-black bg-gray-200 border border-white cursor-default': this.disabled,
        'text-white hover:text-black bg-black hover:bg-white': this.color == 'black' && !this.disabled,
        'text-black hover:text-white bg-white hover:bg-black': this.color == 'white' && !this.disabled,
        'border border-black': this.border && !this.disabled
      }
    }
  }
}
</script>