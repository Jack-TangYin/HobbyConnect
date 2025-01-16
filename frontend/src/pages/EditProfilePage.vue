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
      <button type="submit" class="btn btn-primary me-2">
        Save Profile Changes
      </button>
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
        <input
          type="password"
          id="old_password"
          v-model="passwordForm.old_password"
          class="form-control"
        />
      </div>
      <div class="mb-3">
        <label for="new_password" class="form-label">New Password</label>
        <input
          type="password"
          id="new_password"
          v-model="passwordForm.new_password"
          class="form-control"
        />
      </div>
      <div class="mb-3">
        <label for="confirm_password" class="form-label">Confirm New Password</label>
        <input
          type="password"
          id="confirm_password"
          v-model="passwordForm.confirm_password"
          class="form-control"
        />
      </div>
      <button type="submit" class="btn btn-primary me-2">
        Change Password
      </button>
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
        <!-- Custom Autocomplete Input with Dropdown -->
        <div class="position-relative">
          <input
            type="text"
            id="new_hobby"
            v-model="newHobby"
            class="form-control"
            placeholder="Hobby name"
            @input="onHobbyInput"
            @focus="showSuggestions = true"
          />
          <!-- Dropdown Suggestions: filtered suggestions based on input -->
          <ul
            v-if="showSuggestions && filteredSuggestions.length"
            class="list-group position-absolute w-100"
            style="z-index: 1000; max-height: 200px; overflow-y: auto;"
          >
            <li
              v-for="suggestion in filteredSuggestions"
              :key="suggestion"
              class="list-group-item list-group-item-action"
              @click="selectSuggestion(suggestion)"
              style="cursor: pointer;"
            >
              {{ suggestion }}
            </li>
          </ul>
        </div>

        <button
          type="button"
          class="btn btn-success mt-2 me-2"
          @click="handleAddHobby"
        >
          Add Hobby
        </button>
        <button
          type="button"
          class="btn btn-secondary mt-2"
          @click="clearHobbyInput"
        >
          Clear
        </button>
        <!-- Display error or success message for hobbies section -->
        <span v-if="hobbiesError" class="ms-2 text-danger">{{ hobbiesError }}</span>
        <span v-else-if="hobbiesMessage" class="ms-2 text-success">{{ hobbiesMessage }}</span>
      </div>
      <div>
        <h4>Your Hobbies:</h4>
        <span v-if="user.hobbies && user?.hobbies.length">
          <span
            v-for="hobby in user?.hobbies"
            :key="hobby.id"
            class="badge rounded-pill text-black fs-6 px-3 py-2 me-2 mb-2"
            style="background-color: #fee715"
          >
            {{ hobby.name }}
            <button
              type="button"
              class="btn-close btn-close-white ms-2"
              aria-label="Remove"
              @click="handleRemoveHobby(hobby.id)"
            ></button>
          </span>
        </span>
        <p v-else class="text-muted">You haven’t added any hobbies yet.</p>
      </div>

      <!-- Return Button -->
      <div class="text-center">
        <button type="button" class="btn btn-danger" @click="cancelEdit">
          Return
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, reactive, ref, computed, onBeforeUnmount } from "vue";
import { storeToRefs } from "pinia";
import { useRouter } from "vue-router";
import { getCSRFToken, useAuthStore } from "../stores/authStore";
import { useHobbiesStore } from "../stores/hobbiesStore";
import type { UserFormData, PasswordFormData } from "../types/types";

export default defineComponent({
  name: "EditProfile",
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    const hobbiesStore = useHobbiesStore();
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
    const showSuggestions = ref(false);

    // Reactive message variables for each section
    const profileMessage = ref("");
    const profileError = ref("");
    const passwordMessage = ref("");
    const passwordError = ref("");
    const hobbiesMessage = ref("");
    const hobbiesError = ref("");

    // Computed: filter suggestions based on newHobby input (case-insensitive)
    const filteredSuggestions = computed(() => {
      if (!newHobby.value.trim()) return hobbiesStore.autocompleteSuggestions;
      return hobbiesStore.autocompleteSuggestions.filter((suggestion: string) =>
        suggestion.toLowerCase().includes(newHobby.value.toLowerCase())
      );
    });

    // Fetch hobbies when component mounts
    onMounted(() => {
      hobbiesStore.fetchHobbies();
      document.addEventListener("click", handleClickOutside);
    });
    
    onBeforeUnmount(() => {
      document.removeEventListener("click", handleClickOutside);
    });

    // Submit Profile Changes using PUT
    const submitProfileForm = async (): Promise<void> => {
      try {
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
          profileError.value =
            responseData.message || "Failed to update profile.";
          throw new Error(profileError.value);
        }
        console.log("Profile updated", responseData);
        profileMessage.value =
          responseData.message || "Profile updated successfully.";
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
          passwordError.value =
            responseData.message || "Failed to change password.";
          console.log("passwordError.value", passwordError.value);
          throw new Error(passwordError.value);
        }
        console.log("Password updated", responseData);
        passwordMessage.value =
          responseData.message || "Password changed successfully.";
      } catch (error: any) {
        console.error("Error updating password:", error.message);
        if (error.message) {
          passwordError.value = error.message;
        }
      }
    };

    const clearPasswordForm = (): void => {
      passwordForm.old_password = "";
      passwordForm.new_password = "";
      passwordForm.confirm_password = "";
      passwordMessage.value = "";
      passwordError.value = "";
    };

    // Handle Add Hobby with Store Integration
    const handleAddHobby = async (): Promise<void> => {
      if (!newHobby.value.trim()) return;
      try {
        hobbiesError.value = "";
        hobbiesMessage.value = "";
        const message = await hobbiesStore.addHobby(newHobby.value);
        hobbiesMessage.value = message;
        newHobby.value = "";
        showSuggestions.value = false;
        await authStore.fetchUser();
      } catch (error: any) {
        console.error("Error adding hobby:", error.message);
        hobbiesError.value = error.message;
      }
    };

    // Handle Remove Hobby with Store Integration
    const handleRemoveHobby = async (hobbyId: string): Promise<void> => {
      try {
        hobbiesError.value = "";
        hobbiesMessage.value = "";
        const message = await hobbiesStore.removeHobby(hobbyId);
        hobbiesMessage.value = message;
        await authStore.fetchUser();
      } catch (error: any) {
        console.error("Error removing hobby:", error.message);
        hobbiesError.value = error.message;
      }
    };

    const clearHobbyInput = (): void => {
      newHobby.value = "";
      hobbiesMessage.value = "";
      hobbiesError.value = "";
      showSuggestions.value = false;
    };

    const cancelEdit = (): void => {
      router.back();
    };

    // Handle input for autocomplete suggestions
    const onHobbyInput = (): void => {
      // Simply ensure that suggestions are visible; filtering is handled by computed property.
      showSuggestions.value = true;
    };

    // When a suggestion is clicked, fill in the input and hide suggestions
    const selectSuggestion = (suggestion: string): void => {
      newHobby.value = suggestion;
      showSuggestions.value = false;
    };

    // Hide suggestions when clicking outside the component
    const handleClickOutside = (event: MouseEvent): void => {
      const target = event.target as HTMLElement;
      // If the click is outside our component's area, hide suggestions.
      if (!target.closest(".position-relative")) {
        showSuggestions.value = false;
      }
    };

    return {
      user,
      profileForm,
      passwordForm,
      newHobby,
      showSuggestions,
      filteredSuggestions,
      profileMessage,
      profileError,
      passwordMessage,
      passwordError,
      hobbiesMessage,
      hobbiesError,
      submitProfileForm,
      submitPasswordForm,
      handleAddHobby,
      handleRemoveHobby,
      clearProfileForm,
      clearPasswordForm,
      clearHobbyInput,
      cancelEdit,
      onHobbyInput,
      selectSuggestion,
      hobbiesStore, // Expose the hobbies store for autocomplete suggestions
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
