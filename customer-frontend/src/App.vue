<template>
  <div id="app" class="min-h-screen">
    <router-view />
    <ToastContainer />
  </div>
</template>

<script setup>
import ToastContainer from './components/organisms/ToastContainer.vue'
</script>
