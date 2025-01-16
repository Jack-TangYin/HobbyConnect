const baseUrl = import.meta.env.VITE_APP_API_BASE_URL;

export async function fetchSimilarUsers(minAge: number, maxAge: number, page: number) {
    const query = new URLSearchParams({
        min_age: String(minAge),
        max_age: String(maxAge),
        page: String(page)
    });
    const response = await fetch(`${baseUrl}/api/similar-users/?${query.toString()}`, {
        credentials: 'include', // send cookies if needed
    });
    if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
    }
    return response.json();
}