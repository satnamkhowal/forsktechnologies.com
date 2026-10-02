# Service Content-Gap Audit — 2026-10-02

## Baseline

- 31 legacy `service-*.html` URLs must be preserved during migration.
- All 31 currently use a legacy `Techco` title.
- None has a page-level H1 or canonical tag.
- The reusable PHP service-page system is already available on `main`; it should be adopted only after the hosting/runtime path is verified.

## Implementation priority

1. **Core commercial services:** custom software development, web application development, mobile app development, website development, UI/UX design, cloud solutions, and business consulting.
2. **Cloud specialization:** cloud build/migration, cloud-native consulting, Cloud/DevOps consulting, AWS managed services, and cloud optimization. Confirm distinct buyer intent before treating each as a separate landing page.
3. **Consulting/operations:** IT management, digital transformation, IT audit, change management, process optimization, performance metrics, maintenance/support, and strategy.
4. **Legacy category/archive pages:** keep indexable URLs stable while evaluating whether they need a canonical target, a useful unique purpose, or eventual redirect after a deployed replacement exists.

## Rules for the first migration batch

- Preserve every existing URL and the active visual identity.
- Use verified, service-specific copy; do not publish template testimonials, clients, statistics, awards, certifications, prices, delivery promises, or unverified technologies.
- Add one H1, unique title, description, canonical, useful related-service links, and a functioning enquiry path per migrated page.
- Do not convert HTML URLs to PHP until production hosting and redirects are tested.
- Test desktop/mobile layout, keyboard interaction, links, forms, schema, and final rendered output before merge.

## First batch candidates

- `service-custom-software-development.html`
- `service-web-application-design-and-development.html`
- `service-mobile-app-design-and-development.html`
- `service-website-development.html`
- `service-ui-ux-design-services.html`

The overlapping `service-best-ui-ux-design-services.html` should not be independently expanded until its search intent and canonical relationship to the UI/UX service page are decided.
