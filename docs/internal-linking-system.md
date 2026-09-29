# Forsk Technologies Contextual Internal-Linking System

## Objective

Build a user-first internal-link graph that makes the site's hierarchy clear without exact-match anchor spam, footer link stuffing, or unrelated service cross-linking.

The system uses four principles:

1. **Hierarchy first:** homepage -> services hub -> topical service hubs -> service pages.
2. **Context before quantity:** body links should exist because the surrounding sentence helps the user decide what to read next.
3. **Resources support commercial pages:** articles may link to a closely related hub/service, but should not become link farms.
4. **One clear conversion path:** relevant commercial pages should have one strong contextual route to `/contact/`.

The static repository contains 128 HTML pages and uses `page-map.json` to map pretty/original paths to flattened HTML filenames. Generated date, author, category, tag, service-category, and project-category pages are treated as archive/navigation utilities rather than primary link-equity targets.

---

## Recommended site graph

### Tier 0 — Homepage

- `/`

The homepage should introduce the main capability groups and link to the primary service hub, the major topical hubs, portfolio/proof, and contact. It should **not** list every individual service in body copy or global navigation.

### Tier 1 — Primary hubs

- `/services/`
- `/software-company/`
- `/cloud-solutions/`
- `/business-consulting/`
- `/ai-machine-learning/` where AI/ML is a verified capability

The `/services/` page is the parent discovery hub. The topical hubs fan out to detailed services.

### Tier 2 — Service pages

#### Software / application delivery

- `/service/custom-software-development/`
- `/service/web-application-design-and-development/`
- `/service/mobile-app-design-and-development/`
- `/service/ui-ux-design-services/`
- `/service/website-development/`
- `/service/maintenance-and-customer-support/`

`/service/audit-it-consulting-services/` can be surfaced from the software hub when the surrounding context is technical assessment/discovery, but it should remain cross-functional.

#### Cloud / platform engineering

- `/service/cloud-build-migration/`
- `/service/cloud-native-consulting/`
- `/service/aws-managed-services/`
- `/service/cloud-devops-consulting/`
- `/service/ci-cd-consulting-services/`
- `/service/prometheus-support/`
- `/service/streamlined-cloud-management/`
- `/service/optimize-your-cloud-efficiency/`

#### Business consulting

- `/service/strategic-planning-and-execution/`
- `/service/business-process-optimization/`
- `/service/digital-transformation-consulting/`
- `/service/change-management-solutions/`
- `/service/performance-metrics-and-kpi-development/`
- `/service/market-analysis-and-expansion-strategy/`

#### Broad / cross-functional pages

- `/service/data-tracking-and-security/`
- `/service/it-management-services/`
- `/service/modern-technology-solution/`

These broad pages should link upward to `/services/` unless later content work establishes a more specific parent.

### Tier 1–2 — Company, proof, and conversion

- `/about/`
- `/team/`
- `/our-fields/`
- `/portfolio/`
- `/pricing/`
- `/contact/`

`/contact/` is the primary conversion destination. Company and proof pages should connect to services naturally, but should not carry long SEO link lists.

### Resources

- `/blog/` and its pagination
- Standalone article URLs
- Project/case-study URLs under `/project/`

Articles should link to **one or two directly relevant commercial destinations**, plus a conversion CTA only where it is a natural next step. Case studies should link back to the service/hub that best explains the work, not to unrelated services.

### Archive / utility pages

Do not use these as intentional SEO destinations:

- `/2024/...` date archives
- `/author/...`
- `/category/...`
- `/tag/...`
- `/service-category/...`
- `/project-category/...`

They may remain for navigation/legacy compatibility, but contextual body copy should prefer the main blog, service hubs, service pages, and case studies.

---

## Link-placement rules

### Service hubs

A hub should contain:

- one upward link to `/services/` where useful;
- links to its genuinely relevant child services;
- at most a small number of related resources/case studies;
- one contact CTA.

Avoid adding every other service as a generic “related service.”

### Service pages

Each service page should contain:

- one clear parent-hub link in body copy, a breadcrumb-adjacent summary, or a related-capabilities section;
- zero to three sibling links only when the service relationship is real;
- one contact CTA near the decision point.

Do not repeat the same keyword-rich anchor multiple times.

### Articles

Use contextual sentences such as:

- “If your migration is moving from planning into implementation, our **cloud build and migration approach** explains how we structure the work.”
- “For teams evaluating where AI fits an existing product or workflow, see our **AI and machine learning capabilities**.”

Do not insert blocks such as “cloud services | cloud migration | AWS services | DevOps services” purely for SEO.

### Company and portfolio pages

Use broad, human anchors:

- “Explore our technology services”
- “See the capabilities behind this work”
- “Discuss your project with our team”

Avoid turning the footer or team pages into service-directory duplicates.

### Anchor diversity

Natural anchor language should describe the destination in the sentence. Exact service names are fine when they are genuinely the clearest label, but repeated sitewide exact-match anchors are not the default.

The audit script reports highly concentrated anchor usage for review; it does **not** automatically rewrite anchors.

---

## Current findings to address

### CRITICAL — Homepage role is not cleanly separated

`index.html` currently identifies itself as **Business Consulting – Techco**, so the homepage and consulting-hub roles are not cleanly separated in the repository. Do not duplicate the same contextual link graph across `/` and `/business-consulting/`. Fix the homepage identity/content first, then use the architecture above.

### HIGH — Global navigation is overloaded

The current public homepage exposes the three major hubs and then a long list of individual services, and the same large menu appears again in the mobile/navigation copy. This flattens the hierarchy and makes every service look equally important.

Preferred pattern:

- top level: About, Services, Portfolio/Work, Insights, Contact;
- Services submenu: Software, Cloud, Business Consulting, AI/ML when verified;
- detailed services discovered from the relevant hub (or a restrained secondary mega-menu group if UX testing justifies it).

Do not move the full service list into the footer.

### HIGH — Conversion links should stay on-domain

The current public homepage sends multiple “Get Started Today” CTAs to the original template/demo domain. Replace those with `/contact/` or the approved on-domain enquiry flow.

### HIGH — Legacy/template destinations should not receive link equity

Current public navigation still exposes legacy/template-oriented destinations such as Groot-branded branch/service labels. Only keep links to pages that are verified Forsk Technologies content and intentional parts of the current information architecture.

### PASS — Static local-reference baseline

The existing repository validation reports:

- 128 pages checked;
- 0 missing local references;
- 0 remaining origin links;
- 0 failed local requests.

This means broken local links are **not** being claimed as a current repo problem. The new auditor preserves this check and will fail with exit code `1` if broken internal targets are introduced later.

### HIGH — Duplicate UI/UX intent needs ownership

Both of these URLs exist:

- `/service/best-ui-ux-design-services/`
- `/service/ui-ux-design-services/`

Do not intentionally build equal internal-link authority to both. Choose the canonical/primary service page during the service-architecture audit, then merge/redirect or otherwise resolve the duplicate intent before strengthening links.

### LOW — Legacy/default and archive pages should be demoted

`/hello-world/`, date archives, author archives, broad tag pages, and generic generated category pages should not become deliberate contextual-link targets. Use `/blog/`, relevant articles, or primary service/resource pages instead.

---

## Automated audit

Run from the repository root:

```bash
python scripts/audit_internal_links.py
```

Optional thresholds:

```bash
python scripts/audit_internal_links.py --excessive-unique 60 --weak-contextual 1
```

Generated files:

- `reports/internal-link-audit.csv`
- `reports/internal-link-summary.json`
- `reports/broken-internal-links.csv`
- `reports/cross-cluster-review.csv`

### What the auditor measures

**Contextual links** are links outside header, navigation, footer, breadcrumb, sidebar, and similar repeated template regions.

**Contextual orphan:** a primary page with zero contextual inbound sources.

**Weakly linked:** a primary page with only one contextual inbound source by default.

**Broken internal link:** an internal URL that cannot be resolved to a local HTML file or a `page-map.json` path.

**Excessive links:** more than 60 unique internal targets on one page by default. This is a review threshold, not a search-engine rule.

**Cross-cluster review:** a service-detail page contextually linking to an unrelated service cluster. These are flagged for human review, not automatically removed.

**Anchor warning:** a target whose repeated anchor wording is unusually concentrated. This is a spam-prevention review signal, not an automatic SEO penalty.

---

## Recommendation manifest

See `docs/internal-link-recommendations.csv`.

Every row contains:

- Source URL
- Target URL
- Suggested natural anchor/context
- Reason
- Priority
- Action

Actions:

- `ADD` — safe to add when the source paragraph/section supports the context.
- `HOLD_FOR_CONSOLIDATION` — do not strengthen both duplicate-intent URLs.
- `HOLD_UNTIL_HOME_FIXED` — homepage identity must be corrected before duplicating the consulting link graph.
- `DEMOTE_OR_REMOVE` — do not promote the legacy/default page; remove only through the broader SEO/content cleanup if justified.

The manifest is intentionally selective. It does not prescribe a link between every possible pair of pages.
