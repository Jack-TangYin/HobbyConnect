<template>
    <div>
      <h2>Similar Users</h2>
      <ul>
        <li v-for="user in users" :key="user.id">
          <strong>{{ user.username }}</strong> - Age: {{ user.age }} - Common Hobbies: {{ user.common_hobbies }}
        </li>
      </ul>
      <div>
        <button @click="fetchPreviousPage" :disabled="currentPage === 1">Previous</button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="fetchNextPage" :disabled="currentPage === totalPages">Next</button>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  import { useUserStore } from '../store/userStore';
  
  export default defineComponent({
    setup() {
      const userStore = useUserStore();
      const fetchPreviousPage = () => {
        if (userStore.currentPage > 1) {
          userStore.fetchUsers(0, 100, userStore.currentPage - 1);
        }
      };
      const fetchNextPage = () => {
        if (userStore.currentPage < userStore.totalPages) {
          userStore.fetchUsers(0, 100, userStore.currentPage + 1);
        }
      };
  
      return {
        ...userStore,
        fetchPreviousPage,
        fetchNextPage,
      };
    },
  });
  </script>
  