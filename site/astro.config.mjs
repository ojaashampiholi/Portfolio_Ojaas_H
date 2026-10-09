import { defineConfig } from 'astro/config';
const origin = process.env.SITE_URL || 'http://localhost:4321';
if (process.env.PUBLIC_INDEXABLE === 'true' && (!process.env.SITE_URL || new URL(origin).protocol !== 'https:')) throw new Error('Public builds require an explicit HTTPS SITE_URL.');
export default defineConfig({site: origin, output:'static', trailingSlash:'always', devToolbar:{enabled:false}});
