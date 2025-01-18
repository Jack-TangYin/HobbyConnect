// Type definitions for hobbies
export interface Hobby {
    id: string;
    name: string;
    description: string;
  }
  
  // Type definitions for user data
  export interface UserData {
    userId: string;
    username: string;
    email: string;
    dateOfBirth: string;
    hobbies: Hobby[]; // Array of Hobby objects
    friends: UserData[]; // Recursive structure for nested friends
  }
  
  // Type definitions for the authentication state
  export interface AuthState {
    user: UserData | null; // Nullable for unauthenticated states
    isAuthenticated: boolean;
  }
  
  // Type definitions for user form data (edit profile page)
  export interface UserFormData {
    username: string;
    email: string;
    dateOfBirth: string; // ISO 8601 format
  }
  
  // Type definitions for password form data (edit profile page)
  export interface PasswordFormData {
    old_password: string; // Current password for validation
    new_password: string; // New password
    confirm_password: string; // Confirmation of the new password
  }
  
  // Type definitions for paginated responses (useful for many APIs)
  export interface PaginatedResponse<T> {
    results: T[]; // Array of data items (generic)
    count: number; // Total number of items
    current_page: number; // Current page number
    total_pages: number; // Total number of pages
  }
  
  // Type definitions for similar users (specific to the "fetchSimilarUsers" API)
  export interface SimilarUser {
    id: number;
    username: string;
    age: number; // Age of the user
    common_hobbies: number; // Number of common hobbies
    is_friend: boolean; // Indicates if the user is already a friend
    has_pending_request: boolean; // Indicates if a friend request is pending
  }
  
  export type SimilarUsersResponse = PaginatedResponse<SimilarUser>;
  