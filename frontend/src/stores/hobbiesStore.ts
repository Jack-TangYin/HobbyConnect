// stores/hobbiesStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { Hobby } from '../types/types';
import { getCSRFToken } from './authStore';

export const useHobbiesStore = defineStore('hobbies', () => {
    const hobbies = ref<Hobby[]>([]);
    const isLoading = ref(false);
    const error = ref<string | null>(null);
    const baseUrl = import.meta.env.VITE_APP_API_BASE_URL;
    console.log('baseUrl', baseUrl);

    // Fetch all hobbies from the backend
    const fetchHobbies = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await fetch(`${baseUrl}/api/fetch-hobbies/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                credentials: 'include',
            });
            if (!response.ok) {
                throw new Error('Failed to fetch hobbies.');
            }
            const data = await response.json();
            hobbies.value = data.hobbies;
        } catch (err: any) {
            error.value = err.message || 'An error occurred while fetching hobbies.';
        } finally {
            isLoading.value = false;
        }
    };

    // Add a hobby (handles both existing and new hobbies)
    const addHobby = async (hobbyName: string) => {
        try {
            const response = await fetch(`${baseUrl}/api/update-hobbies/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(), // Ensure you have this utility
                },
                credentials: 'include',
                body: JSON.stringify({
                    action: 'add',
                    hobby: hobbyName.trim(),
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Failed to add hobby.');
            }

            // Optionally, you can update the hobbies list here or refetch
            await fetchHobbies();

            return data.message;
        } catch (err: any) {
            throw new Error(err.message || 'An error occurred while adding the hobby.');
        }
    };

    // Remove a hobby from the user (does not delete from Hobby table)
    const removeHobby = async (hobbyId: string) => {
        try {
            const response = await fetch(`${baseUrl}/api/update-hobbies/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                credentials: 'include',
                body: JSON.stringify({
                    action: 'remove',
                    hobby_id: hobbyId,
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Failed to remove hobby.');
            }

            // Optionally, update the hobbies list here or refetch
            await fetchHobbies();

            return data.message;
        } catch (err: any) {
            throw new Error(err.message || 'An error occurred while removing the hobby.');
        }
    };

    // Get a hobby by name (useful for autocomplete)
    const getHobbyByName = (name: string) => {
        return hobbies.value.find(
            (hobby) => hobby.name.toLowerCase() === name.toLowerCase()
        );
    };

    // Computed property for autocomplete suggestions
    const autocompleteSuggestions = computed(() => {
        return hobbies.value.map((hobby) => hobby.name);
    });

    return {
        hobbies,
        isLoading,
        error,
        fetchHobbies,
        addHobby,
        removeHobby,
        getHobbyByName,
        autocompleteSuggestions,
    };
});
