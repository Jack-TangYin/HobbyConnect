<template>
    <div>
      <label for="minAge">Min Age:</label>
      <input type="number" id="minAge" v-model="minAge" />
      <label for="maxAge">Max Age:</label>
      <input type="number" id="maxAge" v-model="maxAge" />
      <button @click="applyFilter">Apply Filter</button>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from 'vue';
  import { useUserStore } from '../stores/userStore';
  
  export default defineComponent({
    setup() {
      const minAge = ref(0);
      const maxAge = ref(100);
      const userStore = useUserStore();
  
      const applyFilter = () => {
        userStore.fetchUsers(minAge.value, maxAge.value, 1);
      };
  
      return {
        minAge,
        maxAge,
        applyFilter,
      };
    },
  });
  </script>
  