<template>
    <div>
      <h2>Friend Requests</h2>
      <ul>
        <li v-for="request in requests" :key="request.id">
          <span>{{ request.sender }} sent you a friend request</span>
          <button @click="handleRequest(request.id, 'accept')">Accept</button>
          <button @click="handleRequest(request.id, 'reject')">Reject</button>
        </li>
      </ul>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, onMounted } from 'vue';
  import { useFriendRequestStore } from '../stores/friendRequestStore';
  
  export default defineComponent({
    setup() {
      const friendRequestStore = useFriendRequestStore();
  
      onMounted(() => {
        friendRequestStore.fetchRequests();
      });
  
      const handleRequest = (id: number, action: 'accept' | 'reject') => {
        friendRequestStore.handleRequest(id, action);
      };
  
      return {
        requests: friendRequestStore.requests,
        handleRequest,
      };
    },
  });
  </script>
  