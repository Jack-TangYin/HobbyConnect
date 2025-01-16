// Type definitions for user
export interface UserData {
    userId: string;
    username: string;
    email: string;
    dateOfBirth: string;
    hobbies: Hobby[];
}

// Type definitions for hobby
export interface Hobby {
    id: string;
    name: string;
    description: string;
}

// Type definitions for auth state
export interface AuthState {
    user: UserData | null;
    isAuthenticated: boolean;
}
