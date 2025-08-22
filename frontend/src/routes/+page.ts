import type { PageLoad } from './$types';
import { Track } from './schemas'
import { superValidate } from 'sveltekit-superforms';
import { rankingSchema } from './schemas';
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
    const rankingForm = await superValidate(zod4(rankingSchema))
    return {
        rankingForm,
        tracks: getTracks(),
    };
};

