export async function fetchSimilarUsers(minAge: number, maxAge: number, page: number) {
    const response = await fetch(`/api/similar-users/?min_age=${minAge}&max_age=${maxAge}&page=${page}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
    });
    return response.json();
}
