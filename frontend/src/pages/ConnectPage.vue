<template>
  <div class="similar-users">
    <AgeFilter />
    <UsersList />
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import AgeFilter from '../components/AgeFilter.vue';
import UsersList from '../components/UsersList.vue';
import { useUserStore } from '../stores/userStore';

export default defineComponent({
  name: 'SimilarUsers',
  components: {
    AgeFilter,
    UsersList,
  },
  setup() {
    // Use the User Store from Pinia
    const userStore = useUserStore();

    // Load initial users on mount with default filters
    onMounted(async (): Promise<void> => {
      await userStore.fetchUsers(userStore.minAge, userStore.maxAge, 1);
      console.log('Loaded users:', userStore.users);
    });

    return {};
  },
});
</script>

<style scoped>
.similar-users {
  padding: 2rem;
  background-color: #fafafa;
  min-height: 100vh;
}
</style>
