<template>
    <div>
      <AgeFilter />
      <UsersList />
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  import AgeFilter from '../pages/AgeFilter.vue';
  import UsersList from '../pages/UsersList.vue';
  
  export default defineComponent({
    components: {
      AgeFilter,
      UsersList,
    },
  });
  </script>
  