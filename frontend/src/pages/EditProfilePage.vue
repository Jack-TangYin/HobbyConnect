<template>
  <div class="container mt-5">
    <h2>{{ title }}</h2>

    <!-- Profile Edit Form -->
    <form @submit.prevent="submitForm">
      <!-- User Info Fields -->
      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <input
          type="text"
          id="username"
          v-model="formData.username"
          class="form-control"
          required
        />
      </div>

      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input
          type="email"
          id="email"
          v-model="formData.email"
          class="form-control"
          required
        />
      </div>

      <div class="mb-3">
        <label for="date_of_birth" class="form-label">Date of Birth</label>
        <input
          type="date"
          id="date_of_birth"
          v-model="formData.date_of_birth"
          class="form-control"
          required
        />
      </div>

      <!-- Password Change Section -->
      <hr />
      <h3>Change Password</h3>

      <div class="mb-3">
        <label for="old_password" class="form-label">Old Password</label>
        <input
          type="password"
          id="old_password"
          v-model="passwordData.old_password"
          class="form-control"
          required
        />
      </div>

      <div class="mb-3">
        <label for="new_password" class="form-label">New Password</label>
        <input
          type="password"
          id="new_password"
          v-model="passwordData.new_password"
          class="form-control"
          required
        />
      </div>

      <div class="mb-3">
        <label for="confirm_password" class="form-label">Confirm New Password</label>
        <input
          type="password"
          id="confirm_password"
          v-model="passwordData.confirm_password"
          class="form-control"
          required
        />
      </div>

      <button type="submit" class="btn btn-primary">Save Changes</button>
      <button type="button" class="btn btn-secondary ms-2" @click="cancelEdit">Cancel</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

// Define TypeScript interfaces for the form data
interface UserFormData {
  username: string;
  email: string;
  date_of_birth: string;
}

interface PasswordFormData {
  old_password: string;
  new_password: string;
  confirm_password: string;
}

export default defineComponent({
  data() {
    return {
      title: "Edit Profile",
      formData: {
        username: "", // Initialize with user data or from an API
        email: "",
        date_of_birth: "",
      } as UserFormData,
      passwordData: {
        old_password: "",
        new_password: "",
        confirm_password: "",
      } as PasswordFormData,
    };
  },
  methods: {
    async submitForm(): Promise<void> {
      try {
        // Ensure both password fields match
        if (this.passwordData.new_password !== this.passwordData.confirm_password) {
          throw new Error("New passwords do not match.");
        }

        // Prepare the data to be sent
        const data = {
          user: this.formData,
          password: this.passwordData,
        };

        // Send the data to the backend using Fetch API
        const response = await fetch("/api/user/update-profile", {
          method: "POST", // Send a POST request
          headers: {
            "Content-Type": "application/json", // Specify the content type as JSON
          },
          body: JSON.stringify(data), // Convert the data to JSON
        });

        // Check if the response is OK
        if (!response.ok) {
          throw new Error("Failed to update profile");
        }

        // Parse the response as JSON
        const responseData = await response.json();

        // Handle the successful response
        console.log("Profile updated:", responseData);

        // Optionally, add logic to redirect or show a success message
      } catch (error) {
        // Handle errors (e.g., validation or server errors)
        console.error("Error updating profile:", error);
      }
    },
    cancelEdit(): void {
      // Redirect to the profile page
      this.$router.push({ name: "Profile Page" });
    },
  },
});
</script>

<style scoped>
/* Add custom styles if needed */
</style>
