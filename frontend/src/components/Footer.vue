<template>
  <footer class="w-full h-auto flex-shrink-0 p-8 bg-black text-white">
    <div class="container mx-auto flex flex-col md:flex-row items-center md:items-start justify-between">
      <div class="sm:w-1/3 h-auto sm:mt-0 mt-8">
        <div class="text-xl mb-2">Products</div>
        <ul class="hidden md:block list-reset leading-normal">
          <li class="cursor-pointer">All</li>
          <li class="cursor-pointer">Two</li>
          <li class="cursor-pointer">Three</li>
          <li class="cursor-pointer">Four</li>
        </ul>
      </div>

      <div class="sm:w-1/3 h-auto">
        <div class="text-xl mb-2">Something</div>
        <ul class="hidden md:block list-reset leading-normal">
          <li class="cursor-pointer">Lorem</li>
          <li class="cursor-pointer">Ipsum</li>
          <li class="cursor-pointer">Dolor</li>
        </ul>
      </div>

      <div class="sm:w-1/3 h-auto">
        <div class="text-xl mb-2">About</div>
        <ul class="hidden md:block list-reset leading-normal">
          <li class="cursor-pointer">About us</li>
          <li class="cursor-pointer">Contact</li>
          <li class="cursor-pointer">Shipping & returns</li>
        </ul>
      </div>

      <div class="sm:w-1/3 h-auto">
        <p class="text-xl text-center sm:text-left mb-2">Subscribe</p>
        <div class="flex justify-start">
          <input type="text" class="w- sm:w-auto p-2 bg-gray-800 rounded-none text-grey text-sm" placeholder="Your email address">
          <!-- <button class="bg-gray-800 text-white rounded-r h-auto text-xs p-3">Subscribe</button> -->
          <Button class="w-auto text-xs p-3" color="white">Subscribe</Button>
        </div>
      </div>
    </div>

    <div class="w-2/3 mx-auto mt-2 text-center text-sm">© copyright 2021</div>
  </footer>
</template>

<script>
import Button from '@/components/Button.vue'

export default {
  components: {
    Button
  }
}
</script>