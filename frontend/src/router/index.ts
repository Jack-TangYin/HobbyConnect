// Example of how to use Vue Router with TypeScript

import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';

// 1. Import route components
import MainPage from '../pages/MainPage.vue';
import ConnectPage from '../pages/ConnectPage.vue';
import ProfilePage from '../pages/ProfilePage.vue';
import SettingsPage from '../pages/SettingsPage.vue';
import EditProfilePage from '../pages/EditProfilePage.vue';

// Define the base URL based on the environment
const base: string = import.meta.env.MODE === 'development' ? import.meta.env.BASE_URL : '';

// 2. Define routes with TypeScript type safety
const routes: Array<RouteRecordRaw> = [
  { path: '/', name: 'Main Page', component: MainPage },
  { path: '/connect/', name: 'Connect Page', component: ConnectPage },
  { path: '/profile/', name: 'Profile Page', component: ProfilePage },
  { path: '/edit-profile/', name: 'Edit Profile Page', component: EditProfilePage },
  { path: '/settings/', name: 'Settings Page', component: SettingsPage },
];

// 3. Create and configure the router
const router = createRouter({
  history: createWebHistory(base),
  routes,
});

export default router;
