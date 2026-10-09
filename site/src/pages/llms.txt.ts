import type {APIRoute} from 'astro';
import {identities, profile, projects} from '../data/profile';
import {expertiseTerms} from '../data/search-terms';
import writing from '../data/public-writing.json';
import {publishedPosts} from '../data/posts';
export const GET:APIRoute=async({site})=>{
  const origin=site!.href.replace(/\/$/,'');
  const posts=await publishedPosts();
  const lines=[
    `# ${profile.name}`,
    '',
    profile.intro,
    '',
    `Canonical site: ${origin}/`,
    'This file points to the HTML pages. It does not replace them.',
    '',
    '## Pages',
    `- ${origin}/`,
    `- ${origin}/about/`,
    `- ${origin}/work/`,
    ...projects.map(project=>`- ${origin}/work/${project.slug}/`),
    `- ${origin}/writing/`,
    ...posts.map(post=>`- ${origin}/writing/${post.id}/`),
    `- ${origin}/rss.xml`,
    '',
    '## Search phrases',
    'Autocomplete phrases kept only where a project or a public piece matches.',
    ...expertiseTerms.map(term=>`- ${term.query}: ${origin}${term.href}`),
    ...writing.themes.filter(theme=>theme.source==='LinkedIn'||theme.source==='Medium').map(theme=>`- ${theme.label}: ${theme.evidence[0].url}`),
    '',
    '## Native blog',
    'Original posts live at /writing/ and in /rss.xml. Drafts are excluded. External essays are linked, not copied.',
    '',
    '## Same person',
    ...identities.map(item=>`- ${item.name}: ${item.url}`),
    '',
    'Indexing follows /robots.txt. A preview build asks crawlers not to index the site.',
  ];
  return new Response(lines.join('\n')+'\n',{headers:{'Content-Type':'text/plain; charset=utf-8'}});
};
