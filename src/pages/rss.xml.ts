import type {APIRoute} from 'astro';
import {publishedPosts} from '../data/posts';
import {xml} from '../data/xml';
import {siteUrl} from '../data/paths';
export const GET:APIRoute=async({site})=>{const posts=await publishedPosts();return new Response(`<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Ojaas Hampiholi — Writing</title><link>${xml(siteUrl('/',site))}</link><description>Original writing by Ojaas Hampiholi.</description><language>en</language>${posts.map(p=>{const url=siteUrl('/writing/'+p.id+'/',site);return `<item><title>${xml(p.data.title)}</title><description>${xml(p.data.description)}</description><link>${xml(url)}</link><guid isPermaLink="true">${xml(url)}</guid><pubDate>${p.data.published.toUTCString()}</pubDate></item>`}).join('')}</channel></rss>`,{headers:{'Content-Type':'application/rss+xml; charset=utf-8'}});};
