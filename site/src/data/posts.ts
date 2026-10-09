import {getCollection} from 'astro:content';
export async function publishedPosts(){return (await getCollection('writing',p=>!p.data.draft && p.data.published.getTime()<=Date.now())).sort((a,b)=>b.data.published.getTime()-a.data.published.getTime());}
export const formatDate=(date:Date)=>new Intl.DateTimeFormat('en',{year:'numeric',month:'long',day:'numeric',timeZone:'UTC'}).format(date);
