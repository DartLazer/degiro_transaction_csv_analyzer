<template>
  <div>
    <client-only>
      <navbar/>
      <nuxt-page></nuxt-page>
    </client-only>
  </div>
</template>
<script setup>
const transition = {
  name: 'page',
  mode: 'out-in'
}
</script>

<style>
.page-enter-active, .page-leave-active {
  transition: all 0.2s;
}

.page-enter-from, .page-leave-to {
  opacity: 0;
  filter: blur(1rem);
}
</style>