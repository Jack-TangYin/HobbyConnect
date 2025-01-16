import { defineStore } from 'pinia';

export interface User {
    id: number;
    username: string;
    age: number;
    common_hobbies: number;
}

export interface SimilarUsersResponse {
    results: User[];
    count: number;
    current_page: number;
    total_pages: number;
}

const baseUrl = import.meta.env.VITE_APP_API_BASE_URL;


export const useUserStore = defineStore('user', {
    state: () => ({
        users: [] as User[],
        currentPage: 1,
        totalPages: 1,
        // Maintain current filter values so pagination uses these filters
        minAge: 0,
        maxAge: 100,
    }),
    actions: {
        async fetchUsers(minAge: number, maxAge: number, page: number) {
            try {
                // Update current filters in state
                this.minAge = minAge;
                this.maxAge = maxAge;
                const query = new URLSearchParams({
                    min_age: String(minAge),
                    max_age: String(maxAge),
                    page: String(page),
                });
                const response = await fetch(`${baseUrl}/api/fetch-similar-users/?${query.toString()}`, {
                    credentials: 'include', // include cookies if your backend requires authentication
                });
                if (!response.ok) {
                    throw new Error(`Error fetching users: ${response.statusText}`);
                }
                const data: SimilarUsersResponse = await response.json();
                this.users = data.results;
                this.currentPage = data.current_page;
                this.totalPages = data.total_pages;
            } catch (error) {
                console.error(error);
            }
        },
    },
});
