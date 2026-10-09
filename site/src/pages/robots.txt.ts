import type {APIRoute} from 'astro';
export const GET:APIRoute=({site})=>{
  const sitemap=new URL('/sitemap.xml',site);
  const guide=new URL('/llms.txt',site);
  const body=import.meta.env.PUBLIC_INDEXABLE==='true'
    ?`User-agent: *\nAllow: /\n\nUser-agent: GPTBot\nAllow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n\nUser-agent: ChatGPT-User\nAllow: /\n\nUser-agent: Google-Extended\nAllow: /\n\nUser-agent: ClaudeBot\nAllow: /\n\nUser-agent: PerplexityBot\nAllow: /\n\nSitemap: ${sitemap}\n# ${guide}\n`
    :'User-agent: *\nDisallow: /\n';
  return new Response(body,{headers:{'Content-Type':'text/plain; charset=utf-8'}});
};
