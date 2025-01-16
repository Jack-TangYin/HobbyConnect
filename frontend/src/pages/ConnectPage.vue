<template>
  <div class="similar-users">
    <AgeFilter />
    <UsersList />
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import AgeFilter from './AgeFilter.vue';
import UsersList from './UsersList.vue';
import { useUserStore } from '../stores/userStore';

export default defineComponent({
  name: 'SimilarUsers',
  components: {
    AgeFilter,
    UsersList,
  },
  setup() {
    const userStore = useUserStore();

    // Load initial users on mount with default filters
    onMounted(async () => {
      await userStore.fetchUsers(userStore.minAge, userStore.maxAge, 1);
      console.log('userStore', userStore.users);
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
