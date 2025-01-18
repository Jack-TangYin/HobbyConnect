import { defineStore } from 'pinia';
import { UserData, Hobby, AuthState } from '../types/types';

const baseUrl: string = import.meta.env.VITE_APP_API_BASE_URL as string;

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => {
    const storedState = localStorage.getItem('authState');
    try {
      return storedState
        ? (JSON.parse(storedState) as AuthState)
        : {
          user: null,
          isAuthenticated: false,
        };
    } catch {
      console.warn('Invalid authState in localStorage, resetting to default.');
      return {
        user: null,
        isAuthenticated: false,
      };
    }
  },
  getters: {
    userId: (state): string => state.user?.userId ?? '',
    username: (state): string => state.user?.username ?? '',
    email: (state): string => state.user?.email ?? '',
    dateOfBirth: (state): string => state.user?.dateOfBirth ?? '',
    hobbies: (state): Hobby[] => state.user?.hobbies ?? [],
    friends: (state): UserData[] => state.user?.friends ?? [],
  },
  actions: {
    async setCsrfToken(): Promise<void> {
      try {
        await fetch(`${baseUrl}/api/set-csrf-token`, {
          method: 'GET',
          credentials: 'include',
        });
      } catch (error) {
        console.error('Failed to set CSRF token', error);
        throw error;
      }
    },

    async logout(): Promise<void> {
      try {
        const response = await fetch(`${baseUrl}/api/logout/`, {
          method: 'GET',
          headers: {
            'X-CSRFToken': getCSRFToken(),
          },
          credentials: 'include',
        });

        if (response.ok) {
          this.user = null;
          this.isAuthenticated = false;
          this.saveState();
          window.location.href = `${baseUrl}/login`;
        } else {
          console.error('Logout failed with status:', response.status);
        }
      } catch (error) {
        console.error('Logout failed', error);
        throw error;
      }
    },

    async fetchUser(): Promise<void> {
      try {
        const response = await fetch(`${baseUrl}/api/user`, {
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
          },
        });
        if (response.ok) {
          const data: UserData = await response.json();
          console.log('User data', data);
          this.user = data;
          this.isAuthenticated = true;
        } else {
          this.user = null;
          this.isAuthenticated = false;
          window.location.href = `${baseUrl}/login`;
        }
      } catch (error) {
        console.error('Failed to fetch user', error);
        this.user = null;
        this.isAuthenticated = false;
      }
      this.saveState();
    },

    saveState(): void {
      const stateToSave: AuthState = {
        user: this.user,
        isAuthenticated: this.isAuthenticated,
      };
      localStorage.setItem('authState', JSON.stringify(stateToSave));
    },
  },
});

// Utility function for CSRF token
export function getCSRFToken(): string {
  const name = 'csrftoken';
  let cookieValue: string | null = null;

  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === `${name}=`) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }

  if (!cookieValue) {
    throw new Error('Missing CSRF cookie.');
  }
  return cookieValue;
}
