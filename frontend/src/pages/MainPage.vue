<template>
  <div class="mt-5 text-center p-5">
    <h1>Welcome to HobbyConnect!</h1>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "MainPage",
  setup() {
    // Title state
    const title = ref<string>("Main Page");

    return {
      title,
    };
  },
});
</script>

<style scoped>
</style>
