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
        <li v-for="req in requests" :key="req.id" class="dropdown-item">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <strong>{{ req.sender }}</strong>
              <small class="text-muted d-block">Sent at: {{ formatDate(req.timestamp) }}</small>
            </div>
            <div>
              <button class="btn btn-sm btn-success me-1" @click="respond(req.id, 'accept')">&#x2713;</button>
              <button class="btn btn-sm btn-danger" @click="respond(req.id, 'reject')">&#x2717;</button>
            </div>
          </div>
        </li>
      </template>
    </ul>
  </li>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from "vue";
import { useFriendRequestStore } from "../stores/friendRequestStore";

export default defineComponent({
  name: "FriendRequestsDropdown",
  setup() {
    const friendRequestStore = useFriendRequestStore();
    const requests = computed(() => friendRequestStore.requests);
    const loading = ref(false);

    const fetchRequests = async () => {
      loading.value = true;
      await friendRequestStore.fetchRequests();
      loading.value = false;
    };

    const respond = async (requestId: number, action: "accept" | "reject") => {
      try {
        await friendRequestStore.handleRequest(requestId, action);
        alert(`Friend request ${action}ed successfully!`);
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
    onMounted(async () => {
      await fetchRequests();
    });

    return { requests, loading, respond, formatDate };
  },
});
</script>

<style scoped>
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
