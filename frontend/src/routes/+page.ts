import type { PageLoad } from './$types';
import { Track } from './schemas'
import { superValidate } from 'sveltekit-superforms';
import { submitSchema, rankingSchema } from './schemas';
import { zod4 } from 'sveltekit-superforms/adapters';

export const load: PageLoad = async ({ fetch }) => {
    async function getTracks(): Promise<Track[] | string> {
        try {
            const response = await fetch('http://127.0.0.1:8000/tracks/');
            const json = await response.json();
            return response.ok ? (json as Track[]) : (json.detail as string);
        } catch {
            return "Что-то пошло не так.";
        }
    }

    async function getAlbums(): Promise<string[] | string> {
        try {
            const response = await fetch('http://127.0.0.1:8000/albums/');
            const json = await response.json();
            return response.ok ? (json as string[]) : (json.detail as string);
        } catch {
            return "Что-то пошло не так.";
        }
    }

    const submitForm = await superValidate(zod4(submitSchema))
    const rankingForm = await superValidate(zod4(rankingSchema))
    return {
        submitForm,
        rankingForm,
        tracks: getTracks(),
        albums: getAlbums()
    };
};

