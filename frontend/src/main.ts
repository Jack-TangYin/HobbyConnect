import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import { useAuthStore } from './stores/authStore';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

async function initializeApp() {
  const app = createApp(App);

  // Use Pinia and Router
  const pinia = createPinia();
  app.use(pinia);
  app.use(router);

  // Fetch CSRF token before mounting the app
  const authStore = useAuthStore();
  try {
    await authStore.setCsrfToken();
  } catch (error: unknown) {
    console.error('Error setting CSRF token:', error instanceof Error ? error.message : error);
  }

  // Mount the app
  app.mount('#app');
}

// Initialize and mount the app
initializeApp().catch((error) => {
  console.error('Error during app initialization:', error);
});
