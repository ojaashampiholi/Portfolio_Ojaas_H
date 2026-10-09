import { defineConfig } from 'astro/config';
const origin = process.env.SITE_URL || 'http://localhost:4321';
const base = process.env.BASE_PATH;
if (process.env.PUBLIC_INDEXABLE === 'true' && (!process.env.SITE_URL || new URL(origin).protocol !== 'https:')) throw new Error('Public builds require an explicit HTTPS SITE_URL.');
export default defineConfig({site: origin, ...(base && base !== '/' ? {base} : {}), output:'static', trailingSlash:'always', devToolbar:{enabled:false}});
