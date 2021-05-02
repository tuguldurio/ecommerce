<template>
  <div class="fixed top-0 left-0 w-full h-screen z-30 bg-gray-900 bg-opacity-70" @click="close">
  </div>
</template>

<script>
export default {
  methods: {
    close() {
      this.$emit('close')
    }
  }
}
</script>

<style>

</style>