# Forsk Technologies — Master Website Supervisor Work Log

This log is the shared handoff record for website work. Update it after every completed batch so parallel agents can see what changed, what remains, and what must not be overwritten.

## 2026-09-29 — Baseline audit / architecture foundation

**Branch:** `website-supervisor/audit-foundation-2026-09-29`  
**Baseline main commit:** `617753980ef724821dd345b092dec4dbe78c2798`

### Scope inspected

- Repository tree and recent commits
- Root HTML/page inventory
- Homepage (`index.html`) and previous homepage (`index-old.html`)
- `README.md`, `page-map.json`, `validation.json`
- Core stylesheet tokens in `assets/css/style.css`
- Logo inventory in `assets/images/logo/`
- Current public homepage content and navigation
- Search for existing PHP implementation

### Confirmed baseline

- Repository is currently a static Techco theme conversion with 128 root-level HTML pages.
- No PHP implementation was found in the current baseline; reusable PHP includes do not yet exist.
- Existing validation reports 128 pages checked for local links, zero missing local references, zero broken images, zero JavaScript errors, and browser checks at 390px and 1440px.
- Existing forms are not a live enquiry backend: the current static behavior validates input and downloads request data locally.
- `page-map.json` preserves the old WordPress-style URL-to-static-filename mapping and must be treated as URL migration evidence.
- The current design foundation uses Axiforma fonts and the Techco CSS token system. Existing main tokens include `#0044EB` primary, `#020842` dark, `#E3F0FF` light/border, body text `#49515B`, plus existing secondary/accent tokens. Do not introduce random colors; final brand-token adjustments must be checked against the current homepage and approved Forsk logo variants.
- Official Forsk logo variants are present under `assets/images/logo/`, including blue/black/green horizontal, transparent, dark-background, white-background and favicon variants.

### Critical findings

1. **Homepage identity mismatch — BLOCKER**  
   `index.html` is currently the Business Consulting/Techco page rather than a correctly identified Forsk Technologies homepage. Its document title is `Business Consulting – Techco`.

2. **Legacy/template claims live on homepage — BLOCKER**  
   Public homepage currently exposes template/demo material including numerical review/counter claims, Techco testimonials/names, partner/brand-style content, an example Munich address, and Groot Software footer attribution. These cannot be treated as Forsk Technologies facts without verified source data.

3. **Official logo variants are not yet wired into the current homepage header — HIGH**  
   The header/mobile header currently reference `assets/images/site_logo_3-1.svg`, despite the new official Forsk logo variants being available in the logo directory.

4. **Homepage SEO basics incomplete — HIGH**  
   Current homepage lacks a verified Forsk title, meta description and canonical in the inspected source. SEO metadata must be rebuilt without inventing location/business claims.

5. **No reusable PHP common layer — HIGH**  
   Header/navigation/footer/head/scripts/form markup is duplicated across static pages. PHP migration must be incremental and URL-safe, not a bulk rewrite.

6. **Forms are not production-ready — HIGH**  
   Current static forms do not send enquiries to a server/email/database. Do not present them as working lead capture until a backend is deliberately connected and tested.

7. **No root `robots.txt` or XML sitemap identified in the baseline tree — HIGH**  
   Create only after indexable URL decisions are completed so archive/tag/template/demo pages are not accidentally promoted.

8. **Large template/demo inventory requires content verification — HIGH**  
   Team, project, testimonial, client/brand, archive, tag/category and location/branch-style content must be verified before it is kept indexable. Never turn theme demo data into company claims.

### URL/structure protection rules

- Preserve working URLs unless a redirect plan exists.
- Do not rename all `.html` URLs just to introduce PHP.
- Use the existing `page-map.json` as migration evidence before changing paths.
- Do not remove pages only because they look like template exports; first classify whether they have traffic/index value and whether they represent a real Forsk offering.
- Do not overwrite current homepage layout direction while removing unverified content.

### PHP migration approach

Use a controlled common layer, introduced incrementally:

```text
includes/
  head.php
  header.php
  navigation.php
  footer.php
  scripts.php
  enquiry-form.php
  contact-cta.php
  breadcrumbs.php
```

Rules:

- Extract only genuinely repeated markup.
- Preserve current CSS classes and DOM structure wherever possible so visual regressions are minimized.
- Start with a representative low-risk page and the homepage only after the extracted component output is compared against current markup.
- Keep page-specific title/meta/H1/content outside generic includes.
- Do not place fabricated company data inside shared includes.

### Design-system baseline

Current existing CSS baseline (subject to logo/homepage compatibility review):

- Font family: Axiforma Regular / Medium / SemiBold / Bold
- Primary: `#0044EB`
- Dark/headings: `#020842`
- Body text: `#49515B`
- Light surface/border: `#E3F0FF`
- Current secondary token: `#F44380`
- Current info/accent token: `#23BABF`
- Base radius: `10px`
- Small radius token: `20px`
- Pill radius: `50px`
- Transition: `300ms ease`

Do not finalize secondary/accent changes until the homepage and official blue/black/green Forsk logo are compared together. The homepage remains the visual reference.

### Priority queue

| Priority | Task | Status | Notes |
|---|---|---|---|
| P0 | Protect branch + establish shared work log | DONE | This file |
| P0 | Verify homepage against current public deployment and source | DONE | Major template/demo mismatch found |
| P0 | Replace unverified homepage identity/content without redesigning layout | PENDING | Preserve visual structure; requires surgical HTML/component work |
| P0 | Wire official Forsk logo to desktop/mobile header and appropriate footer context | PENDING | Use existing logo variants, not new invented artwork |
| P0 | Establish reusable PHP common layer | PENDING | Incremental, output-equivalent migration |
| P1 | Build page classification: KEEP / REWRITE / NOINDEX / REDIRECT / VERIFY | PENDING | Must precede sitemap |
| P1 | Repair per-page title/meta/canonical/OG/schema/breadcrumbs | PENDING | No keyword stuffing |
| P1 | Implement production enquiry handling | PENDING | Backend requirements must be verified; preserve privacy |
| P1 | Add robots.txt + XML sitemap after indexability decisions | PENDING | Do not sitemap demo/archive junk blindly |
| P1 | Audit all navigation/footer links and remove demo/external placeholders | PENDING | Keep working real internal URLs |
| P2 | Normalize logo usage and favicon | PENDING | Avoid duplicate/ambiguous variants in markup |
| P2 | Audit image alt text and unused/demo assets | PENDING | Do not delete until references are proven unused |
| P2 | Cross-device regression test after each migrated page batch | PENDING | Desktop/tablet/mobile |

### Known blockers / data needed before factual publication

- Verified legal/business identity text, if different from the brand name Forsk Technologies
- Verified company addresses/branches
- Verified clients/partners
- Verified reviews/testimonials
- Verified team members
- Verified awards/certifications
- Verified numerical metrics/statistics

Until verified, omit these claims rather than replacing demo claims with invented alternatives.

### Next recommended action

Create the reusable header/navigation/head/footer skeleton from the existing markup while preserving exact classes and layout, then migrate the homepage as the first controlled page. During that migration, replace the Techco/demo identity, switch to official Forsk logo assets, add safe Forsk homepage metadata, and remove unverified template claims without changing the established page structure.
