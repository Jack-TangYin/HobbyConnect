<template>
    <div>
      <AgeFilter />
      <UsersList />
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  import AgeFilter from '../components/AgeFilter.vue';
  import UsersList from '../components/UsersList.vue';
  
  export default defineComponent({
    components: {
      AgeFilter,
      UsersList,
    },
  });
  </script>
  