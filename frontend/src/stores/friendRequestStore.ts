import { defineStore } from 'pinia';
import { getCSRFToken } from './authStore';

// Define the structure of a FriendRequest
interface FriendRequest {
  id: number;
  sender: string;
  timestamp: string;
}

const baseUrl: string = import.meta.env.VITE_APP_API_BASE_URL as string;

export const useFriendRequestStore = defineStore('friendRequest', {
  state: () => ({
    requests: [] as FriendRequest[],
  }),
  actions: {
    async fetchRequests(): Promise<void> {
      try {
        console.log('Fetching friend requests...');
        const response = await fetch(`${baseUrl}/api/fetch-friend-requests/`, {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
          },
          credentials: 'include',
        });

        if (!response.ok) {
          console.error(`Failed to fetch friend requests: ${response.statusText}`);
          throw new Error(`Error fetching friend requests: ${response.status}`);
        }

        const data = await response.json();
        console.log('Fetched friend requests:', data);
        this.requests = data.friend_requests;
      } catch (error) {
        console.error('Error fetching friend requests:', error);
        throw error; // Re-throw for the caller to handle if needed
      }
    },
    async handleRequest(requestId: number, action: 'accept' | 'reject'): Promise<void> {
      try {
        console.log(`Handling friend request: ${requestId}, action: ${action}`);
        const response = await fetch(`${baseUrl}/api/handle-friend-request/${requestId}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
          },
          credentials: 'include',
          body: JSON.stringify({ action }),
        });

        if (!response.ok) {
          console.error(`Failed to handle friend request: ${response.statusText}`);
          throw new Error(`Error handling friend request: ${response.status}`);
        }

        console.log(`Friend request ${action}ed successfully.`);
        this.requests = this.requests.filter((req) => req.id !== requestId);
      } catch (error) {
        console.error('Error handling friend request:', error);
        throw error; // Re-throw for the caller to handle if needed
      }
    },
  },
});
