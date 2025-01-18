<template>
  <div class="container mt-5">
    <!-- Profile Card -->
    <div class="card shadow-lg border-0">
      <div class="card-header bg-gradient-primary text-center py-4" style="background-color: #101820;">
        <h1 class="fw-bold" style="color: white;">
          <i class="bi bi-person-circle"></i> Your Profile
        </h1>
      </div>
      <div class="card-body p-4">
        <!-- Profile Info -->
        <div class="row mb-4">
          <div class="col-md-4 text-center">
            <div
              class="profile-avatar bg-light rounded-circle mx-auto"
              style="width: 120px; height: 120px; line-height: 120px"
            >
              <i class="bi bi-person-fill fs-1 text-secondary"></i>
            </div>
          </div>
          <div class="col-md-8">
            <h4 class="fw-bold" style="color: #101820;">
              <i class="bi bi-person"></i> Username:
            </h4>
            <p class="text-muted">{{ user?.username }}</p>

            <h4 class="fw-bold" style="color: #101820;">
              <i class="bi bi-envelope"></i> Email:
            </h4>
            <p class="text-muted">{{ user?.email }}</p>

            <h4 class="fw-bold" style="color: #101820;">
              <i class="bi bi-calendar"></i> Date of Birth:
            </h4>
            <p class="text-muted">{{ user?.dateOfBirth }}</p>

            <h4 class="fw-bold" style="color: #101820;">
              <i class="bi bi-heart"></i> Hobbies:
            </h4>
            <div>
              <span v-if="user?.hobbies && user.hobbies.length">
                <span
                  v-for="hobby in user.hobbies"
                  :key="hobby.id"
                  class="badge rounded-pill text-black fs-6 px-3 py-2"
                  style="background-color: #FEE715;"
                >
                  {{ hobby.name }}
                </span>
              </span>
              <p v-else class="text-muted">You haven’t added any hobbies yet.</p>
            </div>
          </div>
        </div>

        <!-- Edit Profile Button -->
        <div class="text-end">
          <router-link id="edit-profile" to="/edit-profile" class="btn btn-primary btn-lg rounded-pill">
            <i class="bi bi-pencil-square"></i> Edit Profile
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useAuthStore } from "../stores/authStore";
import type { UserData } from "../types/types";

export default defineComponent({
  name: "ProfilePage",
  setup() {
    const authStore = useAuthStore();

    // Use the AuthStore to retrieve the user object
    const user: UserData | null = authStore.user;

    return { user };
  },
});
</script>

<style scoped>
</style>
