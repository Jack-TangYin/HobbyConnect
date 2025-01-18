const baseUrl: string = import.meta.env.VITE_APP_API_BASE_URL as string;

interface User {
  id: number;
  username: string;
  age?: number; // Age might not always be available
  common_hobbies?: number; // Number of common hobbies with the logged-in user
  is_friend: boolean;
  has_pending_request: boolean;
}

interface FetchSimilarUsersResponse {
  results: User[];
  count: number;
  current_page: number;
  total_pages: number;
}

export async function fetchSimilarUsers(
  minAge: number,
  maxAge: number,
  page: number
): Promise<FetchSimilarUsersResponse> {
  const query = new URLSearchParams({
    min_age: String(minAge),
    max_age: String(maxAge),
    page: String(page),
  });

  const response = await fetch(`${baseUrl}/api/similar-users/?${query.toString()}`, {
    credentials: 'include', // Send cookies if needed
  });

  if (!response.ok) {
    throw new Error(`Error: ${response.statusText}`);
  }

  const data: FetchSimilarUsersResponse = await response.json();
  return data;
}
