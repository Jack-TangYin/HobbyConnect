<template>
  <div class="users-list">
    <h2>Similar Users</h2>
    <div v-if="userStore.users.length === 0" class="no-results">
      <p>No similar users found. Try adjusting your filters.</p>
    </div>
    <div v-else class="users-container">
      <div v-for="user in userStore.users" :key="user.id" class="user-card">
        <div class="user-info">
          <img
            class="user-avatar"
            :src="'https://ui-avatars.com/api/?name=' + user.username + '&size=128'"
            alt="User Avatar"
          />
          <h3>{{ user.username }}</h3>
          <p id="age"><strong>Age:</strong> {{ user.age }}</p>
          <p><strong>Common Hobbies:</strong> {{ user.common_hobbies }}</p>
        </div>
        <div class="actions">
          <button
            v-if="!user.is_friend && !user.has_pending_request"
            class="friend-btn"
            @click="sendFriendRequest(user.id)"
          >
            🤝 Send Friend Request
          </button>
          <span id="friends" v-else-if="user.is_friend" class="friend-status">
            ✅ Friends
          </span>
          <span v-else class="friend-status">
            ⏳ Request Sent
          </span>
        </div>
      </div>
    </div>
    <div class="pagination">
      <button @click="fetchPreviousPage" :disabled="userStore.currentPage === 1">
        &laquo; Previous
      </button>
      <span>Page {{ userStore.currentPage }} of {{ userStore.totalPages }}</span>
      <button @click="fetchNextPage" :disabled="userStore.currentPage === userStore.totalPages">
        Next &raquo;
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import { useUserStore } from '../stores/userStore';
import { getCSRFToken, useAuthStore } from '../stores/authStore';

const baseUrl: string = import.meta.env.VITE_APP_API_BASE_URL;

export default defineComponent({
  name: 'UsersList',
  setup() {
    // Use Pinia stores
    const userStore = useUserStore();
    const authStore = useAuthStore();

    // Fetch users on component mount
    onMounted(async (): Promise<void> => {
      await userStore.fetchUsers(userStore.minAge, userStore.maxAge, 1);
    });

    // Fetch the previous page of users
    const fetchPreviousPage = (): void => {
      if (userStore.currentPage > 1) {
        userStore.fetchUsers(userStore.minAge, userStore.maxAge, userStore.currentPage - 1);
      }
    };

    // Fetch the next page of users
    const fetchNextPage = (): void => {
      if (userStore.currentPage < userStore.totalPages) {
        userStore.fetchUsers(userStore.minAge, userStore.maxAge, userStore.currentPage + 1);
      }
    };

    // Send a friend request
    const sendFriendRequest = async (receiver_id: number): Promise<void> => {
      try {
        const response = await fetch(`${baseUrl}/api/send-friend-request/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
          },
          credentials: 'include',
          body: JSON.stringify({ receiver_id }),
        });
        if (!response.ok) {
          throw new Error('Failed to send friend request.');
        }
        await userStore.fetchUsers(userStore.minAge, userStore.maxAge, 1);
      } catch (error: unknown) {
        alert('Error sending friend request');
        console.error(error);
      }
    };

    return {
      authStore,
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
  word-wrap: break-word; /* Ensures long text wraps gracefully in all elements */
}

.user-info {
  text-align: center; /* Optional: Aligns all text in the center for a cleaner look */
}

.user-info h3 {
  margin: 0;
  margin-bottom: 0.5rem;
  color: #333;
  font-size: 1rem;
  font-weight: bold;
  white-space: nowrap; /* Prevents text wrapping */
  overflow: hidden; /* Hides overflowing text */
  text-overflow: ellipsis; /* Adds ellipsis for overflowing text */
  max-width: 100%; /* Ensures it stays within the card width */
}

.user-info p {
  margin: 0.25rem 0;
  color: #555;
  font-size: 0.9rem;
  overflow-wrap: break-word; /* Ensures text doesn't overflow its container */
}

.user-avatar {
  border-radius: 50%;
  width: 64px;
  height: 64px;
  margin-bottom: 0.5rem;
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

.friend-status {
  font-size: 0.9rem;
  font-style: italic;
  color: #555;
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
