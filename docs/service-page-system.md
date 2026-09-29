# Forsk Technologies reusable service-page system

## Purpose

Standardize service-page structure without redesigning the site or changing existing URLs. Introduce it page-by-page only after each service's content is verified.

The repository is currently a standalone static export. Existing `.html` service URLs should remain live until hosting/runtime and redirect behavior explicitly support PHP. The renderer outputs only the service-page body so it can later sit between shared head/header/navigation and footer/scripts includes.

## Questions every service page must answer

1. What is the service?
2. Who needs it?
3. What business problem does it solve?
4. What does Forsk Technologies provide?
5. How does the process work?
6. Which technologies/capabilities are relevant and verified?
7. How can the visitor enquire?

## Recommended section order

Use only sections that add real information:

1. Hero
2. Service overview
3. Who needs it
4. Business challenges
5. Solutions / capabilities
6. Process
7. Technology stack — only when verified and relevant
8. Benefits
9. Related services
10. FAQ
11. CTA / enquiry

## Content contract

Each migrated page defines a `$service` array and calls `forsk_render_service_page($service)`.

```php
<?php
require_once __DIR__ . '/includes/service-page.php';

$service = [
    'slug' => 'verified-service-slug',
    'title' => 'Verified service name',
    'eyebrow' => 'Service category',
    'summary' => 'Plain-language summary of the verified service.',
    'overview' => 'What the service covers.',
    'audience' => 'Who normally needs this service.',
    'problem' => 'The business problem the service addresses.',
    'challenges' => ['Verified challenge one'],
    'capabilities' => [
        ['title' => 'Verified capability', 'description' => 'What is provided.'],
    ],
    'process' => [
        ['title' => 'Discovery', 'description' => 'Verified process description.'],
    ],
    'technologies' => [
        // Add only technologies verified for this service.
    ],
    'benefits' => [
        'A realistic, non-guaranteed business benefit.',
    ],
    'related_services' => [
        ['title' => 'Existing related service', 'url' => 'existing-service.html'],
    ],
    'faq' => [
        ['question' => 'Useful customer question?', 'answer' => 'Verified answer.'],
    ],
    'contact_url' => 'contact.html',
    'cta_label' => 'Discuss your requirement',
    // Connect the shared verified form include when available:
    // 'enquiry_form_renderer' => 'render_enquiry_form',
];

forsk_render_service_page($service);
```

## Enquiry behavior

The renderer does not invent or pretend there is a working backend. If a verified shared enquiry-form renderer is connected, it is rendered in the CTA section. Otherwise the page falls back to the existing contact page and clearly treats form integration as pending.

For a real form handler, retain server-side validation, accessible labels/errors, privacy/consent where required, no secrets in page source, and no personal data in public logs.

## Verification rules

Do not publish any of the following unless a repository/site source verifies them:

- client names or logos;
- project/customer counts;
- review totals or ratings;
- success/conversion/uptime percentages;
- awards, certifications, partnerships, or badges;
- staff names/titles;
- Fortune 500 or similar customer claims;
- fees, delivery timelines, SLAs, or guarantees;
- technologies not actually supported for that service.

Generic service benefits should be framed as outcomes the work is **designed to support**, not guaranteed results.

## Existing service URLs to preserve during migration

- `service-audit-it-consulting-services.html`
- `service-aws-managed-services.html`
- `service-best-ui-ux-design-services.html`
- `service-business-process-optimization.html`
- `service-change-management-solutions.html`
- `service-ci-cd-consulting-services.html`
- `service-cloud-build-migration.html`
- `service-cloud-devops-consulting.html`
- `service-cloud-native-consulting.html`
- `service-custom-software-development.html`
- `service-data-tracking-and-security.html`
- `service-digital-transformation-consulting.html`
- `service-it-management-services.html`
- `service-maintenance-and-customer-support.html`
- `service-market-analysis-and-expansion-strategy.html`
- `service-mobile-app-design-and-development.html`
- `service-modern-technology-solution.html`
- `service-optimize-your-cloud-efficiency.html`
- `service-performance-metrics-and-kpi-development.html`
- `service-prometheus-support.html`
- `service-strategic-planning-and-execution.html`
- `service-streamlined-cloud-management.html`
- `service-ui-ux-design-services.html`
- `service-web-application-design-and-development.html`
- `service-website-development.html`

Before migrating a page, confirm its intent is distinct. The two UI/UX URLs and the cluster of cloud-management/optimization/DevOps/native/migration pages especially need an intent check before both/all are treated as separate commercial pages.

## Visual rules

`assets/css/service-page-system.css` is scoped beneath `.forsk-service-page` and inherits the current theme wherever practical. It uses the site's existing blue/dark/cyan direction as fallback values and does not replace global Bootstrap/Elementor/theme styles.

- Keep existing header/footer and page-width conventions.
- Reuse `.container`, `.row`, `.btn`, breadcrumb and Bootstrap accordion behavior.
- Do not introduce an unrelated font family, random gradient, or new global palette.
- Keep one primary CTA per section.
- Maintain readable mobile spacing and practical touch targets.
- Respect reduced-motion preferences.

## Migration checklist per page

- Keep the existing public URL.
- Verify service name, scope, audience, capabilities and technologies.
- Remove demo/template client logos, reviews, fake staff, ratings, statistics, awards and unsupported case studies.
- Replace filler copy with service-specific language.
- Ensure every capability is materially distinct.
- Add related-service links only to real existing URLs.
- Add FAQs only when they help a buyer decide or enquire.
- Confirm CTA destination/form handler actually works.
- Test desktop, tablet and mobile.
- Test keyboard focus and FAQ controls.
- Confirm no duplicate H1, canonical, title or service intent is introduced.
