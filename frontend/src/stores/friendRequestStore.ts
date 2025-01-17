import { defineStore } from 'pinia';
import { getCSRFToken } from './authStore';

interface FriendRequest {
    id: number;
    sender: string;
    timestamp: string;
}

const baseUrl = import.meta.env.VITE_APP_API_BASE_URL;

export const useFriendRequestStore = defineStore('friendRequest', {
    state: () => ({
        requests: [] as FriendRequest[],
    }),
    actions: {
        async fetchRequests() {
            console.log('fetching friend requests');
            const response = await fetch(`${baseUrl}/api/fetch-friend-requests/`, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                credentials: 'include',
            });
            const data = await response.json();
            console.log("fetched friend requests", data);
            this.requests = data.friend_requests;
        },
        async handleRequest(requestId: number, action: 'accept' | 'reject') {
            await fetch(`${baseUrl}/api/handle-friend-request/${requestId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                credentials: 'include',
                body: JSON.stringify({ action }),
            });
            this.requests = this.requests.filter((req) => req.id !== requestId);
        },
    },
});

