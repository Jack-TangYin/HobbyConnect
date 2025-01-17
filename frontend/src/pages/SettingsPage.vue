<template>
    <div class="h3">
      {{ title }}
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from "vue";
  
  export default defineComponent({
    name: "SettingsPage",
    setup() {
      // Define title as a ref with an explicit type
      const title = ref<string>("Settings Page");
  
      return {
        title,
      };
    },
  });
  </script>
  
  <style scoped>
  </style>
  