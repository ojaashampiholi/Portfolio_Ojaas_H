import type {APIRoute} from 'astro';
import {publishedPosts} from '../data/posts';
import {projects} from '../data/profile';
import {xml} from '../data/xml';
import {siteUrl} from '../data/paths';
export const GET:APIRoute=async({site})=>{const paths=['/','/about/','/work/','/writing/',...projects.map(p=>'/work/'+p.slug+'/'),...(await publishedPosts()).map(p=>'/writing/'+p.id+'/')];return new Response(`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${paths.map(p=>`<url><loc>${xml(siteUrl(p,site))}</loc></url>`).join('')}</urlset>`,{headers:{'Content-Type':'application/xml; charset=utf-8'}});};
