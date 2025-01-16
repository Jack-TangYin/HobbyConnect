<template>
  <div class="container mt-5">
    <h2>Edit Profile</h2>
    
    <!-- Core Profile Edit Form -->
    <form @submit.prevent="submitProfileForm" class="mb-4">
      <h3>Profile Details</h3>
      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <!-- If left blank, existing value is retained -->
        <input
          type="text"
          id="username"
          v-model="profileForm.username"
          class="form-control"
          placeholder="Leave blank to keep the same"
        />
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input
          type="email"
          id="email"
          v-model="profileForm.email"
          class="form-control"
          placeholder="Leave blank to keep the same"
        />
      </div>
      <div class="mb-3">
        <label for="dateOfBirth" class="form-label">Date of Birth</label>
        <input
          type="date"
          id="dateOfBirth"
          v-model="profileForm.dateOfBirth"
          class="form-control"
          placeholder="Leave blank to keep the same"
        />
      </div>
      <button type="submit" class="btn btn-primary me-2">Save Profile Changes</button>
      <button type="button" class="btn btn-secondary" @click="clearProfileForm">
        Clear
      </button>
      <!-- Display error or success message for profile section -->
      <span v-if="profileError" class="ms-2 text-danger">{{ profileError }}</span>
      <span v-else-if="profileMessage" class="ms-2 text-success">{{ profileMessage }}</span>
    </form>
    
    <hr />

    <!-- Password Change Form -->
    <form @submit.prevent="submitPasswordForm" class="mb-4">
      <h3>Change Password</h3>
      <div class="mb-3">
        <label for="old_password" class="form-label">Old Password</label>
        <input type="password" id="old_password" v-model="passwordForm.old_password" class="form-control" />
      </div>
      <div class="mb-3">
        <label for="new_password" class="form-label">New Password</label>
        <input type="password" id="new_password" v-model="passwordForm.new_password" class="form-control" />
      </div>
      <div class="mb-3">
        <label for="confirm_password" class="form-label">Confirm New Password</label>
        <input type="password" id="confirm_password" v-model="passwordForm.confirm_password" class="form-control" />
      </div>
      <button type="submit" class="btn btn-primary me-2">Change Password</button>
      <button type="button" class="btn btn-secondary" @click="clearPasswordForm">
        Clear
      </button>
      <!-- Display error or success message for password section -->
      <span v-if="passwordError" class="ms-2 text-danger">{{ passwordError }}</span>
      <span v-else-if="passwordMessage" class="ms-2 text-success">{{ passwordMessage }}</span>
    </form>

    <hr />

    <!-- Hobbies update -->
    <div class="mb-4">
      <h3>Manage Hobbies</h3>
      <div class="mb-3">
        <label for="new_hobby" class="form-label">Add Hobby</label>
        <input
          type="text"
          id="new_hobby"
          v-model="newHobby"
          class="form-control"
          placeholder="Hobby name"
        />
        <button type="button" class="btn btn-success mt-2 me-2" @click="addHobby">Add Hobby</button>
        <button type="button" class="btn btn-secondary mt-2" @click="clearHobbyInput">Clear</button>
        <!-- Display error or success message for hobbies section -->
        <span v-if="hobbiesError" class="ms-2 text-danger">{{ hobbiesError }}</span>
        <span v-else-if="hobbiesMessage" class="ms-2 text-success">{{ hobbiesMessage }}</span>
      </div>
      <div>
        <h4>Your Hobbies:</h4>
        <span v-if="user.hobbies && user?.hobbies.length">
          <span
            v-for="hobby in user.hobbies"
            :key="hobby.id"
            class="badge rounded-pill text-black fs-6 px-3 py-2 me-2 mb-2"
            style="background-color: #FEE715;"
          >
            {{ hobby.name }}
            <button
              type="button"
              class="btn-close btn-close-white ms-2"
              aria-label="Remove"
              @click="removeHobby(hobby.id)"
            ></button>
          </span>
        </span>
        <p v-else class="text-muted">You haven’t added any hobbies yet.</p>
      </div>
    </div>

    <!-- Cancel Button -->
    <div class="text-center">
      <button type="button" class="btn btn-danger" @click="cancelEdit">Cancel</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from "vue";
import { storeToRefs } from "pinia";
import { useRouter } from "vue-router";
import { getCSRFToken, useAuthStore } from "../stores/authStore";
import type { UserFormData, PasswordFormData } from "../types/types";

export default defineComponent({
  name: "EditProfile",
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    const { user } = storeToRefs(authStore);
    const baseUrl = import.meta.env.VITE_APP_API_BASE_URL;

    // Reactive form objects
    const profileForm = reactive<UserFormData>({
      username: "",
      email: "",
      dateOfBirth: "",
    });

    const passwordForm = reactive<PasswordFormData>({
      old_password: "",
      new_password: "",
      confirm_password: "",
    });

    const newHobby = ref("");

    // Reactive message variables for each section
    const profileMessage = ref("");
    const profileError = ref("");
    const passwordMessage = ref("");
    const passwordError = ref("");
    const hobbiesMessage = ref("");
    const hobbiesError = ref("");

    // Submit Profile Changes using PUT
    const submitProfileForm = async (): Promise<void> => {
      try {
        // Clear any previous messages
        profileError.value = "";
        profileMessage.value = "";
        const data = { ...profileForm };
        // Remove empty fields
        Object.keys(data).forEach((key) => {
          const k = key as keyof typeof data;
          if (!data[k]) {
            delete data[k];
          }
        });
        const response = await fetch(`${baseUrl}/api/update-profile/`, {
          method: "PUT",
          headers: { 
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          credentials: "include",
          body: JSON.stringify(data),
        });
        const responseData = await response.json();
        if (!response.ok) {
          // Set error message (displayed in red)
          profileError.value = responseData.message || "Failed to update profile.";
          throw new Error(profileError.value);
        }
        console.log("Profile updated", responseData);
        profileMessage.value = responseData.message || "Profile updated successfully.";
        await authStore.fetchUser();
      } catch (error: any) {
        console.error("Error updating profile:", error.message);
      }
    };

    const clearProfileForm = (): void => {
      profileForm.username = "";
      profileForm.email = "";
      profileForm.dateOfBirth = "";
      profileMessage.value = "";
      profileError.value = "";
    };

    // Submit Password Change using PUT
    const submitPasswordForm = async (): Promise<void> => {
      try {
        passwordError.value = "";
        passwordMessage.value = "";
        if (passwordForm.new_password !== passwordForm.confirm_password) {
          throw new Error("New passwords do not match.");
        }
        const data = { ...passwordForm };
        const response = await fetch(`${baseUrl}/api/change-password/`, {
          method: "PUT",
          headers: { 
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          credentials: "include",
          body: JSON.stringify(data),
        });
        const responseData = await response.json();
        if (!response.ok) {
          passwordError.value = responseData.message || "Failed to change password.";
          console.log('passwordError.value', passwordError.value);
          throw new Error(passwordError.value);
        }
        console.log("Password updated", responseData);
        passwordMessage.value = responseData.message || "Password changed successfully.";
      } catch (error: any) {
        console.error("Error updating password:", error.message);
      }
    };

    const clearPasswordForm = (): void => {
      passwordForm.old_password = "";
      passwordForm.new_password = "";
      passwordForm.confirm_password = "";
      passwordMessage.value = "";
      passwordError.value = "";
    };

    // Add a hobby using PUT
    const addHobby = async (): Promise<void> => {
      if (!newHobby.value.trim()) return;
      try {
        hobbiesError.value = "";
        hobbiesMessage.value = "";
        const response = await fetch(`${baseUrl}/api/update-hobbies/`, {
          method: "PUT",
          headers: { 
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          credentials: "include",
          body: JSON.stringify({
            action: "add",
            hobby: newHobby.value.trim(),
          }),
        });
        const responseData = await response.json();
        if (!response.ok) {
          hobbiesError.value = responseData.message || "Failed to add hobby.";
          throw new Error(hobbiesError.value);
        }
        console.log("Hobby added", responseData);
        hobbiesMessage.value = responseData.message || "Hobby added successfully.";
        await authStore.fetchUser();
      } catch (error: any) {
        console.error("Error adding hobby:", error.message);
      }
    };

    // Remove a hobby using PUT
    const removeHobby = async (hobbyId: string): Promise<void> => {
      try {
        hobbiesError.value = "";
        hobbiesMessage.value = "";
        const response = await fetch(`${baseUrl}/api/update-hobbies/`, {
          method: "PUT",
          headers: { 
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          credentials: "include",
          body: JSON.stringify({
            action: "remove",
            hobby_id: hobbyId,
          }),
        });
        const responseData = await response.json();
        if (!response.ok) {
          hobbiesError.value = responseData.message || "Failed to remove hobby.";
          throw new Error(hobbiesError.value);
        }
        console.log("Hobby removed", responseData);
        hobbiesMessage.value = responseData.message || "Hobby removed successfully.";
        await authStore.fetchUser();
      } catch (error: any) {
        console.error("Error removing hobby:", error.message);
      }
    };

    const clearHobbyInput = (): void => {
      newHobby.value = "";
      hobbiesMessage.value = "";
      hobbiesError.value = "";
    };

    const cancelEdit = (): void => {
      router.back();
    };

    return {
      user,
      profileForm,
      passwordForm,
      newHobby,
      profileMessage,
      profileError,
      passwordMessage,
      passwordError,
      hobbiesMessage,
      hobbiesError,
      submitProfileForm,
      submitPasswordForm,
      addHobby,
      removeHobby,
      clearProfileForm,
      clearPasswordForm,
      clearHobbyInput,
      cancelEdit,
    };
  },
});
</script>

<style scoped>
.ms-2 {
  margin-left: 0.5rem;
}
.text-success {
  color: #28a745;
}
.text-danger {
  color: #dc3545;
}
</style>
