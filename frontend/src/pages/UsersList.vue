<template>
  <div class="user-cards">
    <h2>Similar Users</h2>
    <div class="card" v-for="user in users" :key="user.id">
      <div class="card-content">
        <h3>{{ user.username }}</h3>
        <p>Age: {{ user.age }}</p>
        <p>Hobbies:</p>
        <ul>
          <li v-for="hobby in user.common_hobbies" :key="hobby">{{ hobby }}</li>
        </ul>
        <button @click="addFriend(user.id)">Add Friend</button>
      </div>
    </div>
    <div class="pagination">
      <button @click="fetchPreviousPage" :disabled="currentPage === 1">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="fetchNextPage" :disabled="currentPage === totalPages">Next</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useUserStore } from '../stores/userStore';

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

    const addFriend = async (userId: number) => {
      // Make an API call to send a friend request
      try {
        const response = await fetch(`/api/send-friend-request/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
          body: JSON.stringify({ friend_id: userId }),
        });
        if (response.ok) {
          alert('Friend request sent successfully!');
        } else {
          console.error('Failed to send friend request:', response.statusText);
        }
      } catch (error) {
        console.error('Error sending friend request:', error);
      }
    };

    return {
      ...userStore,
      fetchPreviousPage,
      fetchNextPage,
      addFriend,
    };
  },
});
</script>

<style scoped>
.user-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 16px;
  width: 300px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.card-content {
  text-align: left;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.pagination button {
  margin: 0 10px;
}
</style>
