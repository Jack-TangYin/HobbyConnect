import { defineStore } from 'pinia';
import { fetchSimilarUsers } from '../services/api';

interface User {
    id: number;
    username: string;
    age: number;
    common_hobbies: number;
    hobbies: string[];
}

export const useUserStore = defineStore('user', {
    state: () => ({
        users: [] as User[],
        currentPage: 1,
        totalPages: 1,
    }),
    actions: {
        async fetchUsers(minAge: number, maxAge: number, page: number) {
            const data = await fetchSimilarUsers(minAge, maxAge, page);
            this.users = data.results;
            this.totalPages = Math.ceil(data.count / 10);
            this.currentPage = page;
        },
    },
});
