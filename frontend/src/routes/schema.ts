import { z } from 'zod/v4';

export const searchSchema = z.object({
    source: z.enum(['discogs-master', 'discogs-release', 'spotify']).default('discogs-master'),
    link: z.url('Неверная ссылка.'),
});

export type SearchSchema = typeof searchSchema;