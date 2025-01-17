<template>
  <div class="container mt-5">
    <h2>Edit Profile</h2>

    <!-- Core Profile Edit Form -->
    <form @submit.prevent="submitProfileForm" class="mb-4 mt-4">
      <h3>Profile Details</h3>
      <!-- Profile fields... -->
      <button type="submit" class="btn btn-primary me-2">Save Profile Changes</button>
      <button type="button" class="btn btn-secondary" @click="clearProfileForm">Clear</button>
      <span v-if="profileError" class="ms-2 text-danger">{{ profileError }}</span>
      <span v-else-if="profileMessage" class="ms-2 text-success">{{ profileMessage }}</span>
    </form>

    <hr />

    <!-- Password Change Form -->
    <form @submit.prevent="submitPasswordForm" class="mb-4">
      <h3>Change Password</h3>
      <!-- Password fields... -->
      <button type="submit" class="btn btn-primary me-2">Change Password</button>
      <button type="button" class="btn btn-secondary" @click="clearPasswordForm">Clear</button>
      <span v-if="passwordError" class="ms-2 text-danger">{{ passwordError }}</span>
      <span v-else-if="passwordMessage" class="ms-2 text-success">{{ passwordMessage }}</span>
    </form>

    <hr />

    <!-- Hobbies update -->
    <div class="mb-4">
      <h3>Manage Hobbies</h3>
      <!-- Hobbies management fields... -->
      <div class="text-center">
        <button type="button" class="btn btn-danger" @click="cancelEdit">Return</button>
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
