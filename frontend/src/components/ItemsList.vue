<template>
  <div class="w-full sm:w-3/4 lg:w-2/3 mx-auto mt-16">
    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-0 md:gap-10">
      <div class="flex flex-col items-center h-96"
        v-for="item in items" :key="item.id"
      >
        <router-link class="h-4/5" :to="`/alterations/${item.id}`">
          <img class="h-full object-contain mx-auto cursor-pointer" 
            :src="item.image" alt=""
          >
        </router-link>
        <div class="h-1/5">
          <p class="text-xl text-center">{{ item.name }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    items: Array
  }
}
</script>