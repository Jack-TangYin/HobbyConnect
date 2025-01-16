<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <router-link class="navbar-brand" :to="{ name: 'Main Page' }"
          >Main Page</router-link
        >
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
              <router-link class="nav-link" :to="{ name: 'Main Page' }"
                >Home</router-link
              >
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'Connect Page' }"
                >Connect</router-link
              >
            </li>
          </ul>

          <!-- Right-aligned items with 'Jack' touching the edge -->
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
            <li class="nav-item" style="position: relative; right: -15px">
              <a class="nav-link active" aria-current="page">
                <!-- {{user.username}} -->
                {{authStore.username}}
              </a>
            </li>
            <li
              class="nav-item dropdown"
              style="position: relative; bottom: -2px"
            >
              <a
                class="nav-link dropdown-toggle"
                href="#"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
              </a>
              <!-- Aligns dropdown menu within viewport -->
              <ul class="dropdown-menu dropdown-menu-end">
                <li>
                  <router-link
                    class="dropdown-item"
                    :to="{ name: 'Profile Page' }"
                    >Profile</router-link
                  >
                </li>
                <li>
                  <router-link
                    class="dropdown-item"
                    :to="{ name: 'Settings Page' }"
                    >Settings</router-link
                  >
                </li>
                <li><hr class="dropdown-divider" /></li>
                <li>
                  <button class="dropdown-item" @click="logout()">
                    Sign Out
                  </button>
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

export default defineComponent({
  setup() {
    const authStore = useAuthStore();

    onMounted(async () => {
      try {
        if (!authStore.user) {
          console.log("Fetching user data...");
          await authStore.fetchUser();
        }
        console.log("user: ", authStore.username);
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    });

    const logout = async () => {
      try {
        await authStore.logout();
      } catch (error) {
        console.error(error)
      }
    };
    return { authStore, logout };
  },
  components: { RouterView },
});
</script>

<style scoped></style>
