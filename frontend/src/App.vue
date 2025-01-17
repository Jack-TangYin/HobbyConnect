<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <router-link class="navbar-brand" :to="{ name: 'Main Page' }">HobbyConnect</router-link>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <!-- Main navigation items on the left -->
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'Main Page' }">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'Connect Page' }">Connect</router-link>
            </li>
          </ul>

          <!-- Right-aligned items -->
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0 align-items-center">
            <!-- Notification bell dropdown -->
            <FriendRequestsDropdown />

            <!-- Username and dropdown -->
            <li class="nav-item" style="position: relative; right: -15px">
              <a class="nav-link active" aria-current="page">{{ authStore.username }}</a>
            </li>
            <li class="nav-item dropdown" style="position: relative; bottom: -2px">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              ></a>
              <ul class="dropdown-menu dropdown-menu-end">
                <li>
                  <router-link class="dropdown-item" :to="{ name: 'Profile Page' }">Profile</router-link>
                </li>
                <li>
                  <router-link class="dropdown-item" :to="{ name: 'Settings Page' }">Settings</router-link>
                </li>
                <li><hr class="dropdown-divider" /></li>
                <li>
                  <button class="dropdown-item" @click="logout()">Sign Out</button>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container">
      <RouterView class="flex-shrink-0" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from "vue";
import { RouterView } from "vue-router";
import { useAuthStore } from "./stores/authStore";
import { useHobbiesStore } from "./stores/hobbiesStore";
import { useFriendRequestStore } from "./stores/friendRequestStore";
import FriendRequestsDropdown from "./components/FriendRequestsDropdown.vue";

export default defineComponent({
  name: "App",
  components: { RouterView, FriendRequestsDropdown },
  setup() {
    const authStore = useAuthStore();
    const hobbiesStore = useHobbiesStore();
    const friendRequestStore = useFriendRequestStore();

    onMounted(async () => {
      try {
        if (!authStore.user) {
          console.log("Fetching user data...");
          await authStore.fetchUser();
        }
        if (!hobbiesStore.hobbies.length) {
          console.log("Fetching hobbies data...");
          await hobbiesStore.fetchHobbies();
        }
        if (!friendRequestStore.requests.length) {
          console.log("Fetching friend requests...");
          await friendRequestStore.fetchRequests();
        }

        console.log("User:", authStore.user?.username);
        console.log("Hobbies:", hobbiesStore.hobbies);
      } catch (error: unknown) {
        console.error("Error initializing app:", error instanceof Error ? error.message : error);
      }
    });

    const logout = async (): Promise<void> => {
      try {
        await authStore.logout();
      } catch (error: unknown) {
        console.error("Error during logout:", error instanceof Error ? error.message : error);
      }
    };

    return { authStore, logout };
  },
});
</script>

<style scoped></style>
