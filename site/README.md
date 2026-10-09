# Ojaas portfolio — local trial

Astro 7, TypeScript, native CSS, static HTML. Requires Node compatible with Astro 7 and Python 3. No client framework or database.

## Run

- `npm install`
- `npm run dev` — local preview at http://localhost:4321
- `npm run check`
- `npm run build` — refresh public writing, then generate static output
- `npm run verify` — validate generated HTML, links, schema, feeds, and index policy
- `python3 scripts/test-writing.py` — date boundaries and safe importer behavior
- `python3 scripts/test-publishing.py` — temporary published/future post fixtures, then restore clean trial build

## Authoring

Profile and project content: `src/data/profile.ts`. Add native Markdown posts under `src/content/writing/`. The collection validates title, description, publication date, optional update date, tags, and draft state. Posts default to drafts; both drafts and future-dated posts are excluded from pages, sitemap, and RSS. The first-post file is a hidden template, not an article attributed to Ojaas.

## Public writing and inferred themes

`npm run refresh:writing` fetches Medium RSS, Substack RSS, and Cosmic Notebook's homepage plus archive. The same refresh runs before each build. Development refresh is explicit; visitors do not trigger scraping. No recurring scheduler has been configured.

The importer stores plain-text metadata and brief public excerpts in `src/data/public-writing.json`; no remote HTML executes. URLs are restricted to the supplied publication hosts. Tracking parameters are removed, repeated titles are deduplicated, future dates are excluded, and network failures retain the source's last successful snapshot with a visible stale-data notice.

Current interests are a **rule-based inference prototype**, not an LLM service. Six transparent topic rules use titles, excerpts, source tags and known publication context over a rolling 60-day window. Each result links to evidence. The Substack fiction theme describes the publication; fictional events are not treated as biographical facts or personal beliefs. Topic rules can be expanded as the writing changes. Feed/archive availability bounds coverage; public availability is not proof of search-engine indexing.

The homepage shows one latest article from each source; the writing hub shows three per source so daily astronomy notes do not displace technical work. Original-platform links remain external; the native RSS feed contains only original native posts.

## Public launch

This trial has not been deployed. It defaults to noindex and robots Disallow. Choose the final domain, then set `SITE_URL=https://your-domain` and `PUBLIC_INDEXABLE=true` when building. Public mode requires an explicit HTTPS origin. Serve `dist/` through a static host with directory-index support and a real 404 response using `404.html`. Test deployed headers, status codes, crawl access and performance before launch. Metadata and readable HTML support discovery; search or AI-answer inclusion cannot be guaranteed.

Raw résumé/profile PDFs and phone numbers are not included in public assets. Source-derived professional claims are tracked in ../docs/CONTENT-SOURCES.md.
