<template>
  <div class="container mt-5">
    <h2>Edit Profile</h2>

    <!-- Core Profile Edit Form -->
    <form @submit.prevent="submitProfileForm" class="mb-4 mt-4">
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
      <button id="update-profile" type="submit" class="btn btn-primary me-2">
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
      <button id="update-password" type="submit" class="btn btn-primary me-2">
        Change Password
      </button>
      <button id="clear-password" type="button" class="btn btn-secondary" @click="clearPasswordForm">
        Clear
      </button>
      <!-- Display error or success message for password section -->
      <span v-if="passwordError" class="ms-2 text-danger">{{ passwordError }}</span>
      <span v-else-if="passwordMessage" class="ms-2 text-success">{{ passwordMessage }}</span>
    </form>

    <hr />

    <!-- Hobbies update -->
    <div class="mb-4">
      <h3 id="click-here">Manage Hobbies</h3>
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
          id="add-hobby"
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
      <div id="hobbies-list">
        <h4>Your Hobbies:</h4>
        <span v-if="user.hobbies && user?.hobbies.length">
          <span
            v-for="hobby in user?.hobbies"
            :key="hobby.id"
            :id="hobby.name"
            class="badge rounded-pill text-black fs-6 px-3 py-2 me-2 mb-2"
            style="background-color: #fee715"
          >
            {{ hobby.name }}
            <button
              :id="'delete-' + hobby.name"
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
        <button id="return-button" type="button" class="btn btn-danger" @click="cancelEdit">
          Return
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, reactive, ref, computed, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import { useAuthStore, getCSRFToken } from "../stores/authStore";
import { useHobbiesStore } from "../stores/hobbiesStore";
import type { UserFormData, PasswordFormData } from "../types/types";

export default defineComponent({
  name: "EditProfile",
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    const hobbiesStore = useHobbiesStore();
    const { user } = storeToRefs(authStore);
    const baseUrl = import.meta.env.VITE_APP_API_BASE_URL as string;

    // Reactive forms
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

    const newHobby = ref<string>("");
    const showSuggestions = ref<boolean>(false);

    // Messages
    const profileMessage = ref<string>("");
    const profileError = ref<string>("");
    const passwordMessage = ref<string>("");
    const passwordError = ref<string>("");
    const hobbiesMessage = ref<string>("");
    const hobbiesError = ref<string>("");

    const filteredSuggestions = computed<string[]>(() => {
      if (!newHobby.value.trim()) return hobbiesStore.autocompleteSuggestions;
      return hobbiesStore.autocompleteSuggestions.filter((suggestion: string) =>
        suggestion.toLowerCase().includes(newHobby.value.toLowerCase())
      );
    });

    // Fetch hobbies on mount
    onMounted(() => {
      hobbiesStore.fetchHobbies();
      document.addEventListener("click", handleClickOutside);
    });

    onBeforeUnmount(() => {
      document.removeEventListener("click", handleClickOutside);
    });

    // Submit profile changes
    const submitProfileForm = async (): Promise<void> => {
      try {
        const data = { ...profileForm };
        Object.keys(data).forEach((key) => {
          if (!data[key as keyof typeof data]) delete data[key as keyof typeof data];
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
        if (!response.ok) throw new Error(responseData.message || "Failed to update profile.");

        profileMessage.value = responseData.message || "Profile updated successfully.";
        await authStore.fetchUser();
      } catch (error: unknown) {
        profileError.value = error instanceof Error ? error.message : "Error updating profile.";
      }
    };

    // Submit password changes
    const submitPasswordForm = async (): Promise<void> => {
      try {
        if (passwordForm.new_password !== passwordForm.confirm_password) {
          throw new Error("New passwords do not match.");
        }

        const response = await fetch(`${baseUrl}/api/change-password/`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          credentials: "include",
          body: JSON.stringify(passwordForm),
        });

        const responseData = await response.json();
        if (!response.ok) throw new Error(responseData.message || "Failed to change password.");

        passwordMessage.value = responseData.message || "Password changed successfully.";
      } catch (error: unknown) {
        passwordError.value = error instanceof Error ? error.message : "Error changing password.";
      }
    };

    // Utility functions (clear forms, handle hobby input, etc.)
    const clearProfileForm = (): void => {
      profileForm.username = "";
      profileForm.email = "";
      profileForm.dateOfBirth = "";
      profileMessage.value = "";
      profileError.value = "";
    };

    const clearPasswordForm = (): void => {
      passwordForm.old_password = "";
      passwordForm.new_password = "";
      passwordForm.confirm_password = "";
      passwordMessage.value = "";
      passwordError.value = "";
    };

    const cancelEdit = (): void => {
      router.back();
    };

    const handleClickOutside = (event: MouseEvent): void => {
      const target = event.target as HTMLElement;
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
      clearProfileForm,
      clearPasswordForm,
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
