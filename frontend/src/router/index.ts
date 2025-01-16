// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'

// 1. Define route components.
// These can be imported from other files
import MainPage from '../pages/MainPage.vue';
import ConnectPage from '../pages/ConnectPage.vue';
import ProfilePage from '../pages/ProfilePage.vue';
import SettingsPage from '../pages/SettingsPage.vue';
import EditProfilePage from '../pages/EditProfilePage.vue';
import SimilarUsersPage from '../pages/SimilarUsersPage.vue';

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/', name: 'Main Page', component: MainPage },
        { path: '/connect/', name: 'Connect Page', component: ConnectPage },
        { path: '/profile/', name: 'Profile Page', component: ProfilePage },
        { path: '/edit-profile/', name: 'Edit Profile Page', component: EditProfilePage },
        { path: '/settings/', name: 'Settings Page', component: SettingsPage },
        {path: '/similar-users/', name: 'Similar Users Page', component: SimilarUsersPage},
    ]
})

export default router
