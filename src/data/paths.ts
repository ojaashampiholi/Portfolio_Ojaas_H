const prefix = import.meta.env.BASE_URL || '/';

export function sitePath(path: string): string {
  const root = prefix.endsWith('/') ? prefix : `${prefix}/`;
  if (!path || path === '/') return root;
  return `${root}${path.replace(/^\//, '')}`;
}

export function siteUrl(path: string, origin: URL | undefined): string {
  if (!origin) return sitePath(path);
  return new URL(sitePath(path), origin).href;
}
