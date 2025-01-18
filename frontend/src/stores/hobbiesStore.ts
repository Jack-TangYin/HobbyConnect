import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { Hobby } from '../types/types';
import { getCSRFToken } from './authStore';

export const useHobbiesStore = defineStore('hobbies', () => {
  const hobbies = ref<Hobby[]>([]);
  const isLoading = ref<boolean>(false);
  const error = ref<string | null>(null);
  const baseUrl: string = import.meta.env.VITE_APP_API_BASE_URL as string;

  // Fetch all hobbies from the backend
  const fetchHobbies = async (): Promise<void> => {
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

      const data: { hobbies: Hobby[] } = await response.json();
      hobbies.value = data.hobbies;
    } catch (err: unknown) {
      error.value = (err instanceof Error) ? err.message : 'An error occurred while fetching hobbies.';
    } finally {
      isLoading.value = false;
    }
  };

  // Add a hobby (handles both existing and new hobbies)
  const addHobby = async (hobbyName: string): Promise<string> => {
    try {
      const response = await fetch(`${baseUrl}/api/update-hobbies/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
        },
        credentials: 'include',
        body: JSON.stringify({
          action: 'add',
          hobby: hobbyName.trim(),
        }),
      });

      const data: { message: string } = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Failed to add hobby.');
      }

      await fetchHobbies(); // Optionally refetch the hobbies

      return data.message;
    } catch (err: unknown) {
      const errorMessage = (err instanceof Error) ? err.message : 'An error occurred while adding the hobby.';
      throw new Error(errorMessage);
    }
  };

  // Remove a hobby from the user (does not delete from Hobby table)
  const removeHobby = async (hobbyId: string): Promise<string> => {
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

      const data: { message: string } = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Failed to remove hobby.');
      }

      await fetchHobbies(); // Optionally refetch the hobbies

      return data.message;
    } catch (err: unknown) {
      const errorMessage = (err instanceof Error) ? err.message : 'An error occurred while removing the hobby.';
      throw new Error(errorMessage);
    }
  };

  // Get a hobby by name (useful for autocomplete)
  const getHobbyByName = (name: string): Hobby | undefined => {
    return hobbies.value.find((hobby) => hobby.name.toLowerCase() === name.toLowerCase());
  };

  // Computed property for autocomplete suggestions
  const autocompleteSuggestions = computed<string[]>(() => {
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
