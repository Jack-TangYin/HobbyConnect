<template>
  <div class="age-filter">
    <label for="minAge">Min Age:</label>
    <input type="number" id="minAge" v-model.number="minAge" />

    <label for="maxAge">Max Age:</label>
    <input type="number" id="maxAge" v-model.number="maxAge" />

    <button @click="applyFilter">Apply Filter</button>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useUserStore } from '../stores/userStore';

export default defineComponent({
  name: 'AgeFilter',
  setup() {
    const minAge = ref(0);
    const maxAge = ref(100);
    const userStore = useUserStore();

    const applyFilter = () => {
      userStore.fetchUsers(minAge.value, maxAge.value, 1);
    };

    return {
      minAge,
      maxAge,
      applyFilter,
    };
  },
});
</script>

<style scoped>
.age-filter {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 5px;
  margin-bottom: 1.5rem;
}

.age-filter label {
  font-weight: bold;
}

.age-filter input {
  width: 70px;
  padding: 0.25rem;
  border: 1px solid #ccc;
  border-radius: 3px;
}

.age-filter button {
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.age-filter button:hover {
  background-color: #0056b3;
}
</style>
