<template>
  <div>
    <AgeFilter />
    <UsersList />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AgeFilter from "../pages/AgeFilter.vue";
import UsersList from "../pages/UsersList.vue";

export default defineComponent({
    setup() {
        
        return {
            AgeFilter,
            UsersList,
        };
    },
  components: {
    AgeFilter,
    UsersList,
  },
});
</script>
