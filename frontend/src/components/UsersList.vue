<template>
  <div class="users-list">
    <h2>Similar Users</h2>
    <div v-if="userStore.users.length === 0" class="no-results">
      No similar users found.
    </div>
    <div v-else class="users-container">
      <div v-for="user in userStore.users" :key="user.id" class="user-card">
        <div class="user-info">
          <h3>{{ user.username }}</h3>
          <p>Age: {{ user.age }}</p>
          <p>Common Hobbies: {{ user.common_hobbies }}</p>
        </div>
        <button class="friend-btn" @click="sendFriendRequest(user.id)">
          Send Friend Request
        </button>
      </div>
    </div>
    <div class="pagination">
      <button @click="fetchPreviousPage" :disabled="userStore.currentPage === 1">
        Previous
      </button>
      <span>Page {{ userStore.currentPage }} of {{ userStore.totalPages }}</span>
      <button @click="fetchNextPage" :disabled="userStore.currentPage === userStore.totalPages">
        Next
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import { useUserStore } from '../stores/userStore';
import { getCSRFToken } from '../stores/authStore';

const baseUrl = import.meta.env.VITE_APP_API_BASE_URL;

export default defineComponent({
  name: 'UsersList',
  setup() {
    const userStore = useUserStore();

    onMounted(async () => {
      await userStore.fetchUsers(userStore.minAge, userStore.maxAge, 1);
    });

    const fetchPreviousPage = () => {
      if (userStore.currentPage > 1) {
        userStore.fetchUsers(userStore.minAge, userStore.maxAge, userStore.currentPage - 1);
      }
    };
    const fetchNextPage = () => {
      if (userStore.currentPage < userStore.totalPages) {
        userStore.fetchUsers(userStore.minAge, userStore.maxAge, userStore.currentPage + 1);
      }
    };

    const sendFriendRequest = async (receiver_id: number) => {
      try {
        const response = await fetch(`${baseUrl}/api/send-friend-request/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
          },
          credentials: 'include',
          body: JSON.stringify({ receiver_id: receiver_id }),
        });
        if (!response.ok) {
          throw new Error('Failed to send friend request.');
        }
        const result = await response.json();
        alert(result.message || 'Friend request sent successfully!');
      } catch (error) {
        alert('Error sending friend request');
        console.error(error);
      }
    };

    return {
      userStore,
      fetchPreviousPage,
      fetchNextPage,
      sendFriendRequest,
    };
  },
});
</script>

<style scoped>
.users-list {
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
}

.users-list h2 {
  text-align: center;
  margin-bottom: 1.5rem;
}

.no-results {
  text-align: center;
  font-style: italic;
  color: #888;
}

.users-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}

.user-card {
  background: #ffffff;
  border: 1px solid #ddd;
  border-radius: 5px;
  width: 240px;
  padding: 1rem;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.user-info h3 {
  margin: 0;
  margin-bottom: 0.5rem;
  color: #333;
}

.user-info p {
  margin: 0.25rem 0;
  color: #555;
  font-size: 0.9rem;
}

.friend-btn {
  margin-top: 1rem;
  padding: 0.5rem;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.friend-btn:hover {
  background-color: #218838;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 1.5rem;
  gap: 1rem;
}

.pagination button {
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
