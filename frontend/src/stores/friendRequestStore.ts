import { defineStore } from 'pinia';

interface FriendRequest {
    id: number;
    sender: string;
    timestamp: string;
}

export const useFriendRequestStore = defineStore('friendRequest', {
    state: () => ({
        requests: [] as FriendRequest[],
    }),
    actions: {
        async fetchRequests() {
            const response = await fetch('/api/friend-requests/', {
                headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
            });
            const data = await response.json();
            this.requests = data;
        },
        async handleRequest(requestId: number, action: 'accept' | 'reject') {
            await fetch(`/api/friend-requests/${requestId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
                body: JSON.stringify({ action }),
            });
            this.requests = this.requests.filter((req) => req.id !== requestId);
        },
    },
});
