<template>
  <li class="nav-item dropdown position-relative">
    <!-- Notification bell button with badge if there are pending requests -->
    <a
      class="nav-link dropdown-toggle"
      href="#"
      role="button"
      data-bs-toggle="dropdown"
      aria-expanded="false"
    >
      <i class="bi bi-bell"></i>
      <!-- Badge for notifications -->
      <span v-if="requests.length" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
        {{ requests.length }}
      </span>
    </a>
    <!-- Dropdown menu -->
    <ul class="dropdown-menu dropdown-menu-end">
      <li v-if="loading" class="dropdown-item text-center">
        Loading...
      </li>
      <li v-else-if="!requests.length" class="dropdown-item text-center">
        No friend requests
      </li>
      <template v-else>
        <li v-for="req in requests" :key="req.request_id" class="dropdown-item">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <strong>{{ req.sender_username }}</strong>
              <small class="text-muted d-block">Sent at: {{ formatDate(req.created_at) }}</small>
            </div>
            <div>
              <button class="btn btn-sm btn-success me-1" @click="respond(req.request_id, 'approve')">✓</button>
              <button class="btn btn-sm btn-danger" @click="respond(req.request_id, 'reject')">✕</button>
            </div>
          </div>
        </li>
      </template>
    </ul>
  </li>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";

interface FriendRequest {
  request_id: number;
  sender_id: number;
  sender_username: string;
  created_at: string;
}

export default defineComponent({
  name: "FriendRequestsDropdown",
  setup() {
    const requests = ref<FriendRequest[]>([]);
    const loading = ref(false);

    const fetchRequests = async () => {
      loading.value = true;
      try {
        const res = await fetch("/api/list-friend-requests/", {
          credentials: "include",
        });
        const data = await res.json();
        requests.value = data.requests || [];
      } catch (error) {
        console.error("Error fetching friend requests:", error);
      } finally {
        loading.value = false;
      }
    };

    const respond = async (requestId: number, action: string) => {
      try {
        const res = await fetch("/api/respond-friend-request/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
          body: JSON.stringify({ request_id: requestId, action }),
        });
        const result = await res.json();
        alert(result.message);
        // Refresh the list after responding
        await fetchRequests();
      } catch (error) {
        alert("Error processing friend request");
        console.error(error);
      }
    };

    const formatDate = (dateStr: string) => {
      const date = new Date(dateStr);
      return date.toLocaleString();
    };

    // Fetch requests on component mount
    onMounted(() => {
      fetchRequests();
    });

    return { requests, loading, respond, formatDate };
  },
});
</script>

<style scoped>
/* Basic styling for badge and dropdown items */
.fa-bell {
  font-size: 1.2rem;
}

.badge {
  position: absolute;
  top: 0;
  right: 0;
  transform: translate(50%, -50%);
}
</style>
