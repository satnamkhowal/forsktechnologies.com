# PHP include architecture audit

This refactor is intentionally conservative. It extracts only blocks proven byte-identical across multiple root pages and leaves page-specific markup in place.

## Shared includes created

- `includes/footer.php` — exact repeated footer block, including its trailing whitespace; detected on **123** HTML pages.
- `includes/scripts.php` — exact repeated common JavaScript bundle, including its trailing whitespace; detected on **116** HTML pages.

## Converted pages

**128** root pages were converted from `.html` files to internal `.php` files. Existing public/internal links remain `.html`; `.htaccess` internally maps a missing historical `.html` file to its matching PHP implementation without changing the browser URL.

Footer include used on **123** converted pages. Common scripts include used on **116** converted pages.

## Intentionally not extracted

- **Header/navigation:** kept page-local because the export contains page-specific current-menu/current-page classes. A static shared header would mark the wrong navigation item on some pages.
- **Head:** kept page-local because titles and Elementor/post-specific CSS links differ by page. This preserves existing SEO metadata and CSS order; page-specific metadata remains directly configurable per page.
- **Enquiry/contact CTA:** not promoted to a global include because the audit did not prove one exact reusable block across the converted page set.
- **Breadcrumbs:** retained page-local because their content is page-specific and no normalization is required for this safe pass.

## Compatibility rules

- Existing `.html` links and visible URLs are preserved.
- Relative asset paths remain unchanged because browser-visible URLs remain the historical root-level `.html` URLs.
- Direct requests for converted `.php` URLs redirect back to `.html` on Apache/LiteSpeed via `.htaccess`.
- Unconverted `.html` pages continue to work as static files.
- Converted pages require PHP plus Apache/LiteSpeed rewrite support; a purely static host cannot execute the includes.

## Validation

Every converted page is PHP-linted, rendered with PHP CLI, and compared byte-for-byte with its original HTML source. The build fails on any rendering difference. It also checks for duplicate include markers and verifies each removed historical HTML file has exactly one PHP replacement.

## Converted legacy filenames

- `about.html`
- `ai-machine-learning.html`
- `archive-2024-06-07.html`
- `archive-2024-06-08-page-2.html`
- `archive-2024-06-08.html`
- `archive-2024-06-page-2.html`
- `archive-2024-06-page-3.html`
- `archive-2024-06.html`
- `archive-2024-11-13.html`
- `archive-2024-11.html`
- `archive-2024-page-2.html`
- `archive-2024-page-3.html`
- `archive-2024-page-4.html`
- `archive-2024.html`
- `author-admin-page-2.html`
- `author-admin-page-3.html`
- `author-admin-page-4.html`
- `author-admin.html`
- `blog-page-2.html`
- `blog-page-3.html`
- `blog-page-4.html`
- `blog.html`
- `business-consulting.html`
- `category-business-page-2.html`
- `category-business.html`
- `category-cloud-solution.html`
- `category-cybersecurity-page-2.html`
- `category-cybersecurity.html`
- `category-it-solution.html`
- `category-mobile-app-page-2.html`
- `category-mobile-app.html`
- `category-tech-trends-page-2.html`
- `category-tech-trends.html`
- `category-techsolutions.html`
- `category-uncategorized.html`
- `category-ux-design-page-2.html`
- `category-ux-design.html`
- `cloud-security-best-practices-company-should-know.html`
- `contact.html`
- `future-proofing-your-business-with-cloud-modernization.html`
- `harnessing-the-power-of-ai-and-machine-learning-in-business.html`
- `hello-world.html`
- `index-old.html`
- `index.html`
- `innovation-in-action-how-consulting-firms-foster-creative-solutions.html`
- `insider-perspectives-on-it-solutions-with-techco-thought-leaders.html`
- `leading-the-digital-age-with-groundbreaking-it-technologies.html`
- `our-fields.html`
- `portfolio.html`
- `pricing.html`
- `project-astarte-medical.html`
- `project-cae-blue-phantom.html`
- `project-category-3d-design.html`
- `project-category-analysis.html`
- `project-category-app-design.html`
- `project-category-computer-software.html`
- `project-category-healthcare.html`
- `project-category-helpdesk.html`
- `project-category-marketing.html`
- `project-category-real-estate.html`
- `project-category-technology.html`
- `project-category-web-design.html`
- `project-cloud-migration-and-integration-project-it-solutions-portfolio.html`
- `project-dashboard-design.html`
- `project-driving-digital-transformation-explore-the-depth-of-our-it-projects.html`
- `project-explore-our-it-solutions-portfolio-for-public-sector-organizations-copy.html`
- `project-explore-our-it-solutions-portfolio-for-public-sector-organizations.html`
- `project-liberkeys.html`
- `project-mobile-app-design.html`
- `project-pioneering-progress-exploring-the-evolution-and-impact-of.html`
- `project-revolutionizing-it-strategies-a-closer-look-at-our-dynamic-it-solutions.html`
- `project-tech-triumphs-celebrating-our-achievements-in-it-solutions.html`
- `project-technology-solution.html`
- `project-unlocking-potential-explore-our-comprehensive-it-portfolio.html`
- `seamless-integration-of-hybrid-and-multi-cloud-environments.html`
- `service-audit-it-consulting-services.html`
- `service-aws-managed-services.html`
- `service-best-ui-ux-design-services.html`
- `service-business-process-optimization.html`
- `service-category-consultation.html`
- `service-category-management.html`
- `service-category-mobile-app.html`
- `service-category-solution.html`
- `service-category-strategy.html`
- `service-category-transfer.html`
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
- `services.html`
- `software-company.html`
- `tag-app-dev-page-2.html`
- `tag-app-dev.html`
- `tag-consultants.html`
- `tag-cybersecurity.html`
- `tag-data-page-2.html`
- `tag-data-page-3.html`
- `tag-data.html`
- `tag-it.html`
- `tag-optimization.html`
- `tag-solution-page-2.html`
- `tag-solution-page-3.html`
- `tag-solution.html`
- `tag-startup.html`
- `tag-techsolutions.html`
- `team-details.html`
- `team.html`
- `the-next-big-thing-quantum-computing-and-its-business-applications.html`
- `top-cloud-migration-strategies-for-growing-businesses.html`
- `transforming-your-business-with-consulting-to-drive-operational-excellence.html`
- `unlocking-new-possibilities-with-advanced-cloud-computing-solutions.html`
