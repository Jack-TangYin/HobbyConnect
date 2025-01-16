// Type definitions for user
export interface UserData {
    userId: string;
    username: string;
    email: string;
    dateOfBirth: string;
    hobbies: Hobby[];
    friends: UserData[];
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

// Type definitions for user form data (edit profile page)
export interface UserFormData {
    username: string;
    email: string;
    dateOfBirth: string;
}

// Type definitions for password form data (edit profile page)
export interface PasswordFormData {
    old_password: string;
    new_password: string;
    confirm_password: string;
}
