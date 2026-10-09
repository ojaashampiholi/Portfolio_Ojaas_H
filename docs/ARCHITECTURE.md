# Trial architecture — provisional

## Decision
Select Astro with TypeScript, static output, native CSS, and Markdown content collections for the trial. The portfolio and articles are present in the initial HTML response. Add client JavaScript only when an actual interaction needs it. This content-led site does not currently need a database, authentication, or a React runtime. A browser-based CMS can be added later if the authoring preference requires one.

## Data ownership
Version-controlled profile and project records; native articles in Markdown/MDX or an equivalent structured content collection. External writing entries store title, original URL, publication, date when known, and an original short contextual description. Do not copy external articles wholesale.

## Route model
- / — identity, selected evidence, writing, contact path
- /work/ — project index
- /work/[slug]/ — problem, role, implementation, decisions, evidence, limitations
- /about/ — verified background and identity links
- /writing/ — native posts and clearly marked external references
- /writing/[slug]/ — native articles
- /rss.xml, /sitemap.xml, /robots.txt
- Real 404 page for unknown routes

## Search and answer engines
Semantic HTML; descriptive titles; unique summaries; canonical URLs; discoverable internal links; Person/WebSite and applicable Article structured data that matches visible content. Use a configured production origin for all absolute URLs. Explicitly distinguish preview indexing policy from public launch policy.

Search/answer-engine inclusion cannot be guaranteed. No special AEO certification or universal LLM-crawler compliance standard is assumed. An optional llms.txt is not a substitute for HTML, links, robots policy, or sitemap.

## Failure paths
Invalid content fails validation/build. Drafts do not enter production routes or feeds. Missing optional images/metrics are omitted. Broken internal links fail verification. Unknown URLs return 404. Contact links use real supplied destinations; no pretend submission form.

## Verification plan
Production build and content validation; fetch rendered HTML without JavaScript; check canonical and structured-data consistency; verify feed/sitemap exclusions; browser desktop/mobile and keyboard checks; inspect console/network errors and screenshots. Record evidence in REVIEW.md.

## Pending decisions
Publishing workflow, final framework, production domain, public contact, and verified personal content.

## Decision comparison

| Option | Fit | Tradeoff |
| --- | --- | --- |
| Astro static + Markdown | Selected: portfolio and native publication | Rebuild after content changes; CMS optional later |
| Next.js with server rendering | Useful if the site becomes an application | Additional runtime complexity for the current reading/navigation journeys |
| Handwritten static pages | Simple initial delivery | Repeated metadata and weaker content validation as the blog grows |

## Source checks, 2026-09-27
- Astro official content-collections documentation confirms schema-based content and static route generation: https://docs.astro.build/en/guides/content-collections/
- Astro official rendering documentation confirms prerendered HTML by default: https://docs.astro.build/en/guides/on-demand-rendering/
- Google states foundational SEO practices apply to its AI search features: https://developers.google.com/search/docs/appearance/ai-features
- Registry version observed: Astro 7.3.5. No package has been installed yet; compatibility and build behavior remain to be checked.

## Content provenance
User supplied https://www.linkedin.com/in/ojaashampiholi/ but both web retrieval and browser access failed. No professional-history claims have been inferred from that URL. Resume, Medium, Substack, and Cosmic Notebook sources are expected later.

## Implemented trial and subsequent decisions
Astro 7.3.5 is installed with TypeScript validation and a lockfile in `site/`. Nine static HTML pages implement the portfolio. Native Markdown article routes, RSS, sitemap, Person/WebSite/BlogPosting JSON-LD, and production-origin/indexability controls are implemented. Public launch and a final domain remain pending.

A prebuild Python importer now fetches Medium RSS, Substack RSS, and Cosmic Notebook HTML indexes. It persists a last-successful per-source snapshot, normalizes plain-text metadata and allowed URLs, deduplicates titles, and derives evidence-linked themes over 90 days using explicit rules. No client-side scraping or LLM API dependency. Latest articles and inferred themes are rendered into HTML. No scheduler is configured: refresh happens on build or explicit refresh.

The owner has requested more visual personality and will select liked elements from the four references in DESIGN-REFERENCES.md. The current design is retained as a baseline until that feedback arrives.

## Writing refresh revision

Build-time refresh now includes a known public LinkedIn permalink, validated using root SocialMediaPosting JSON-LD author and datePublished. Comments are excluded. LinkedIn is partial coverage, not an account-wide discovery integration. Add verified post permalinks to the importer to extend coverage; RSS feeds are also bounded by what their publishers expose.

The rolling window is 90 days. Deterministic source-specific phrase rules identify supported themes, rather than an LLM inventing interests. Unmatched new subject areas require extending RULES. Each section links inferred phrases to original evidence. A source failure preserves that source's last successful snapshot and is disclosed. The refresh runs on builds, not visits; production scheduling is not configured. The static HTML includes all writing and summaries for crawlers.
