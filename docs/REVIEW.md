# Trial review

## Completed design checks

| Pair | Contrast | Result |
| --- | --- | --- |
| #17212b on #ffffff | 16.29:1 | PASS (normal text >= 4.5:1) |
| #17212b on #f3f5f7 | 14.91:1 | PASS (normal text >= 4.5:1) |
| #495563 on #ffffff | 7.60:1 | PASS (normal text >= 4.5:1) |
| #495563 on #f3f5f7 | 6.95:1 | PASS (normal text >= 4.5:1) |
| #185abd on #ffffff | 6.49:1 | PASS (normal text >= 4.5:1) |
| #185abd on #f3f5f7 | 5.94:1 | PASS (normal text >= 4.5:1) |

Contrast calculated using WCAG relative luminance. This checks planned token pairs, not a rendered page.

## Verification status

| Area | Status | Evidence / remaining work |
| --- | --- | --- |
| Playbook alignment | PASS | Brief, design direction, data ownership, failure paths, and verification plan recorded |
| Rendering strategy | PASS — documentation review only | Official Astro documentation supports static HTML and content collections |
| Professional content | BLOCKED | LinkedIn inaccessible; headline/About requested, further sources forthcoming |
| Production build | NOT CHECKED | Implementation pending |
| Browser desktop/mobile | NOT CHECKED | Implementation pending |
| Keyboard / focus / enlargement | NOT CHECKED | Implementation pending |
| Metadata / feeds / crawler directives | NOT CHECKED | Implementation pending |
| Hosting | NOT CHECKED | No site registered or deployed |

Architecture documentation checks are not evidence that the website is built or browser-verified.

## Implementation update — September 27, 2026
This supersedes the earlier implementation-pending rows above.

- PASS: Astro check, zero errors/warnings/hints.
- PASS: static production build; nine final HTML pages.
- PASS: generated-output checks for unique titles/descriptions, one h1, absolute canonical URLs, valid schema JSON, internal links and fragments, no client scripts, RSS/sitemap, draft exclusions, and preview index policy.
- PASS: temporary native-article fixture produced an article route, BlogPosting metadata and RSS entry. Future/draft fixtures were excluded. Fixtures removed and trial rebuilt.
- PASS: public-mode build tested with a non-deployed example origin, then restored to unindexed local mode.
- PASS: homepage → work → project navigation in browser. Initial desktop screenshot and 390px homepage/writing/project layouts inspected, no measured horizontal overflow on project/writing pages.
- PASS: planned normal-text contrast pairs range from 5.94:1 to 16.29:1.
- PASS: writing importer fetched all three sources; combined Cosmic homepage/archive fixes an observed omission of its newest ten posts.
- PASS: importer tests cover 90-day expiry, future exclusion, evidence rules, HTML stripping, URL allowlisting, tracking removal, empty-feed failure.
- NOT CHECKED: full keyboard journey, 200% text enlargement, reduced-motion browser emulation, deployed 404 behavior, production performance and real search indexing.
- No public deployment. Final visual direction awaits user preference feedback on reference sites.

## Playful palette contrast

Measured with WCAG relative luminance after the coral and blue marks were added. Body text stays ink on paper. Coral and blue are used as fills, tag borders, and project numbers.

| Pair | Contrast | Result |
| --- | --- | --- |
| #232f35 on #faf8f2 | 12.93:1 | PASS |
| #515e62 on #faf8f2 | 6.32:1 | PASS |
| #245f66 on #faf8f2 | 6.81:1 | PASS |
| #232f35 on #f0eee5 | 11.81:1 | PASS |
| #515e62 on #f0eee5 | 5.78:1 | PASS |
| #232f35 on #f8e4dc | 11.19:1 | PASS |
| #232f35 on #e4eef8 | 11.69:1 | PASS |
| #ffffff on #c24b32 | 4.83:1 | PASS |
| #ffffff on #1d5c99 | 6.90:1 | PASS |
| #c24b32 on #faf8f2 | 4.55:1 | PASS |
| #1d5c99 on #faf8f2 | 6.50:1 | PASS |

## September 28 writing and visual revision

- Public refresh: 49 entries; LinkedIn, Medium, Substack and Cosmic Notebook all fetched successfully.
- Python tests passed: inclusive 90-day boundary, future exclusion, source isolation, public LinkedIn root metadata parsing (not comments), URL validation and empty-feed handling.
- Astro check: zero errors or warnings. Production build and generated HTML verification passed (9 pages, metadata/schema, canonical URLs, internal links, RSS/sitemap, draft exclusion and preview noindex).
- Browser inspected at desktop 1440px and mobile 390px. Writing sections fit without horizontal overflow. Homepage retains leadership-first order.
- Writing index navigated to Fiction; heading position confirmed. Pause checkbox computed animation state changed to paused; keyboard Space resumed motion.
- Reduced-motion support verified in CSS; OS reduced-motion emulation was not exercised.
- Not deployed. Production indexing remains intentionally disabled in the local trial.
