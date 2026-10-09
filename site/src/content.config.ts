import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { glob } from 'astro/loaders';
const writing=defineCollection({loader:glob({pattern:'**/*.md',base:'./src/content/writing'}),schema:z.object({title:z.string().min(1),description:z.string().min(1),published:z.coerce.date(),updated:z.coerce.date().optional(),draft:z.boolean().default(true),tags:z.array(z.string()).default([])})});
export const collections={writing};
