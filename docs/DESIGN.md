# Design direction — engineering editorial

## Rationale
Recruiters need a fast statement of fit. Founders need evidence of judgment and delivery. Technical peers need enough depth to inspect the work. Use a strong typographic introduction followed by project evidence and an editorial writing index; let readers move from summary into depth.

## Tokens
- Background: #ffffff; secondary surface: #f3f5f7
- Primary text: #17212b; secondary text: #495563
- Accent: #185abd, used consistently for links and selected emphasis
- Rules: #d3dae2; no decorative shadows
- Body: system sans-serif initially, 18px / 1.65
- Headlines: same family, strong weight, responsive 40–76px, line-height 1.08
- Metadata: system monospace, 14px / 1.5
- Reading width: 68ch; layout maximum: 1200px
- Spacing: 4, 8, 12, 16, 24, 32, 48, 64, 96px
- Corners: 4px on controls; square editorial sections

## Composition
Asymmetric desktop introduction with a compact identity column and larger statement/evidence column. Full-width ruled project entries with short summaries and clear routes to technical detail. Writing presented as a publication index, with native and external entries explicitly distinguished. Narrow screens use one column and a wrapping navigation; no horizontal carousel.

## Controls and states
Use ordinary semantic links for navigation, visible underlines in prose, and 3px accent focus outlines with offset. Active navigation uses both text weight and an underline. Interactive targets have generous padding. A genuine empty writing state is preferable to invented publications.

## Motion
Content and navigation appear immediately. Optional color/border hover transitions at 120ms; no scroll reveals, parallax, or autoplay. Reduced-motion preference disables transitions. No motion library needed.

## Guardrails
No fabricated statistics, skill percentages, testimonials, employment history, client logos, or project screenshots. No decorative AI imagery. Technical diagrams are included only when grounded in actual projects. The homepage must communicate professional relevance before aesthetic effects.

## Verification pending
Measure token contrast; inspect actual text wrapping, keyboard focus, 200% enlargement, and mobile/desktop screenshots after implementation. This document describes intent, not completed checks.

## References
AI Engineering Playbook BRIEF/DESIGN/REVIEW workflow.
Pinned taste-skill c184364c58658b2f131b4ae8bd3d206cabb3deee: audience-led direction, coherent palette, typography hierarchy, responsive and accessible controls. Its optional framework and motion defaults are subordinate to this content-first brief.
Pinned gstack digest b9706f3635b6a545f46fae607ae9d6bcbfb69b91: reuse native features first, complete the actual journey, record verification.

## Playful technical publication

Warm paper and teal remain the reading surface. Coral `#c24b32` and blue `#1d5c99` mark diagrams, tags, and project numbers. Washes `#f8e4dc` and `#e4eef8` sit behind those marks. Body text stays ink on paper.

Nunito carries display headings. Source Sans 3 carries body copy. Courier Prime remains the label face. Georgia is the display fallback.

Project entries include a small hand-drawn SVG: audience ranking, a payment decision path, a two-stage résumé check, and a paper-to-cluster path for LitLens. Article pages keep a title, a one-line summary, then the reading column.

Path strokes draw once. Hover lifts a diagram by a few pixels. Both stop when motion is paused or `prefers-reduced-motion` is set. Navigation text appears immediately.

## September 28 revision: professional writing first

The selected direction combines an editorial writing index inspired by Maggie Appleton, restrained playful motion inspired by Josh Comeau, and clearly separated leadership evidence inspired by Brittany Chiang. No assets or code were copied. Warm paper, dark teal, serif display headings and self-hosted Courier Prime section labels replace the initial all-sans treatment.

Professional writing combines LinkedIn short posts and Medium essays. Fiction and The Cosmic Notebook have independent section anchors, smaller headings and quieter homepage summaries. Each subtitle derives only from its own sources within the trailing 90 days and links to evidence. The homepage keeps leadership and work ahead of writing.

Motion uses CSS transforms: a slow writing-index asterisk, directional arrows and small hover responses. All looping motion is gated by prefers-reduced-motion:no-preference. A keyboard-accessible native Pause motion checkbox stops animations; no browser JavaScript is shipped.

## September 29 revision: one path through the page

The visible title is Builder. One sentence assigns the hat: data scientist at Samsung, ML engineer on the Amazon payments work, AI engineer on LitLens and CVPilot. The homepage is that sentence, a project list, a short writing list, and the invitation. The coral margin, résumé card, three plates, and writing-page side index are gone. Search phrases live on the work page only. Pause motion sits in the footer. Identity links, including the earlier portfolio repository, still use `rel="me"` and Person `sameAs`. Cosmic Notebook and Substack stay off that identity list.

## October 9 revision: a personal document

The page should read as one person's notebook. The references are [nishkeni.github.io](https://nishkeni.github.io/) and [minjekim.com](https://minjekim.com/), not a product homepage. From the first: a quiet role line in coral above the title, hairline rules, and no second marketing button. From the second: work and writing as dated lists, a title with one sentence. Nunito stays, at a lighter weight and a tighter line height. Courier Prime stays on dates and labels. Source Sans 3 stays on body text. Teal stays on links and focus. Coral stays on the homepage role line and on project numbers.

Left out on purpose: the portrait, journal masthead, equation, citation bars, booking button, and reader count from the first site; the photo carousel from the second. Also left out: SaaS landing-page galleries, UI kits, glass panels, bento grids, and product design files such as Linear, Stripe, or Vercel. Search phrases stay words, not filter chips. The round OH monogram stays. Email stays inside mailto links.
