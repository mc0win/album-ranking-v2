import type { PageLoad } from "../$types"

async function getAlbums(fetch: (input: RequestInfo | URL, init?: RequestInit) => Promise<Response>): Promise<string[] | string> {
    try {
        const response = await fetch('http://127.0.0.1:8000/albums/');
        const json = await response.json();
        return response.ok ? (json as string[]) : (json.detail as string);
    } catch {
        return "Что-то пошло не так.";
    }
}

export const load: PageLoad = async ({ fetch }) => {
    return {
        albums: getAlbums(fetch)
    }
}