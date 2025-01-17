import { defineStore } from 'pinia';

// Define the User and API response types
export interface User {
  id: number;
  username: string;
  age: number;
  common_hobbies: number;
  is_friend: boolean;
  has_pending_request: boolean;
}

export interface SimilarUsersResponse {
  results: User[];
  count: number;
  current_page: number;
  total_pages: number;
}

// Define the base URL for the API
const baseUrl: string = import.meta.env.VITE_APP_API_BASE_URL as string;

export const useUserStore = defineStore('user', {
  state: () => ({
    users: [] as User[],
    currentPage: 1,
    totalPages: 1,
    minAge: 0,
    maxAge: 100,
  }),
  actions: {
    async fetchUsers(minAge: number, maxAge: number, page: number): Promise<void> {
      try {
        // Update state with current filter values
        this.minAge = minAge;
        this.maxAge = maxAge;

        const query = new URLSearchParams({
          min_age: String(minAge),
          max_age: String(maxAge),
          page: String(page),
        });

        const response = await fetch(`${baseUrl}/api/fetch-similar-users/?${query.toString()}`, {
          credentials: 'include',
        });

        if (!response.ok) {
          throw new Error(`Error fetching users: ${response.statusText}`);
        }

        const data: SimilarUsersResponse = await response.json();
        this.users = data.results;
        this.currentPage = data.current_page;
        this.totalPages = data.total_pages;
      } catch (error) {
        console.error('Error fetching users:', error instanceof Error ? error.message : error);
      }
    },
  },
});
