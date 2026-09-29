# Forsk Technologies Internal-Link Audit Findings

Audit baseline: refined CI run on `main` after commit `90406350180775e083a553307a350adcc54829fc`.

## Summary

| Metric | Result |
|---|---:|
| HTML pages scanned | 129 |
| Internal links evaluated | 16,406 |
| Broken internal links | 0 |
| Absolute orphan pages | 1 |
| Contextual orphan primary pages | 7 |
| Weak primary pages | 30 |
| Pages above navigation/excessive-link review thresholds | 76 |
| Cross-cluster service links requiring review | 0 |
| Anchor-concentration warnings | 6 |

The thresholds are review signals, not search-engine limits. An absolute orphan has no internal inbound link at all. A contextual orphan may be reachable from global navigation/archive chrome but has no contextual inbound body link from another primary page.

## Absolute orphan

- `/index-old.html`

This is a legacy backup-style page. Do not build authority to it. Remove it from deployment or explicitly noindex/archive it if it must remain available for maintenance.

## Contextual orphan primary pages

- `/ai-machine-learning/`
- `/business-consulting/`
- `/cloud-solutions/`
- `/our-fields/`
- `/seamless-integration-of-hybrid-and-multi-cloud-environments/`
- `/software-company/`
- `/the-next-big-thing-quantum-computing-and-its-business-applications/`

The four main service hubs should receive natural in-body links from the homepage and `/services/`. `/our-fields/` should only be promoted if it remains a useful company/capabilities page. The two article orphans should receive contextual links only from genuinely related resource/service contexts; do not force them into unrelated pages merely to cure an orphan.

## Weak primary pages

These pages currently have only one contextual inbound source under the audit definition:

- `/blog/`
- `/cloud-security-best-practices-company-should-know/`
- `/future-proofing-your-business-with-cloud-modernization/`
- `/harnessing-the-power-of-ai-and-machine-learning-in-business/`
- `/leading-the-digital-age-with-groundbreaking-it-technologies/`
- `/project/astarte-medical/`
- `/project/cae-blue-phantom/`
- `/project/cloud-migration-and-integration-project-it-solutions-portfolio/`
- `/project/driving-digital-transformation-explore-the-depth-of-our-it-projects/`
- `/project/explore-our-it-solutions-portfolio-for-public-sector-organizations-copy/`
- `/project/explore-our-it-solutions-portfolio-for-public-sector-organizations/`
- `/project/liberkeys/`
- `/project/revolutionizing-it-strategies-a-closer-look-at-our-dynamic-it-solutions/`
- `/project/tech-triumphs-celebrating-our-achievements-in-it-solutions/`
- `/project/technology-solution/`
- `/service/audit-it-consulting-services/`
- `/service/aws-managed-services/`
- `/service/best-ui-ux-design-services/`
- `/service/ci-cd-consulting-services/`
- `/service/cloud-build-migration/`
- `/service/cloud-devops-consulting/`
- `/service/cloud-native-consulting/`
- `/service/custom-software-development/`
- `/service/maintenance-and-customer-support/`
- `/service/mobile-app-design-and-development/`
- `/service/optimize-your-cloud-efficiency/`
- `/service/prometheus-support/`
- `/service/streamlined-cloud-management/`
- `/service/web-application-design-and-development/`
- `/top-cloud-migration-strategies-for-growing-businesses/`

The commercially important weak pages are the individual service pages. Each should receive a parent-hub link from the relevant service hub and should link back upward with natural wording. Project pages should be linked from portfolio/relevant service contexts, not sitewide.

## Excessive-link review

76 pages cross the configured review threshold because they expose more than 35 unique non-contextual/navigation targets or more than 60 unique internal targets. This is dominated by repeated template/archive navigation rather than contextual body links.

The affected groups are:

- date archives under `/2024/`
- author archives under `/author/admin/`
- blog pagination under `/blog/page/`
- most `/category/` archives
- most `/tag/` archives
- all `/service-category/` archives
- all `/project-category/` archives
- `/blog/`
- `/hello-world/`
- the standalone article pages, which generally carry about 39–40 unique non-contextual targets

Do not fix this by moving the same link list into the footer. For retained articles/resources, simplify secondary navigation so the article remains primary, keep a restrained route back to `/blog/`, and add only one or two genuinely related commercial destinations. Generated archive/tag pages should not be deliberate link-equity targets unless they provide real user value.

The full page-level list is generated in `reports/internal-link-audit.csv` on every CI run.

## Broken internal links

None detected in the refined run.

The repository's pre-existing static validation also reports zero missing local references and zero failed local requests, so broken-link findings should only be added if a future audit actually finds them.

## Irrelevant cross-linking

No service-detail-to-unrelated-service-cluster contextual links were detected. This is a PASS, not an invitation to create cross-cluster links.

Broad services such as IT management or data/security should generally route upward to `/services/` unless a more specific relationship is visible in page copy. The audit will flag future service-detail links that cross clearly different topic clusters for human review.

## Anchor-concentration review

Six targets triggered the review threshold:

- `/software-company/` — `software company`, 100% of 258 observed occurrences
- `/cloud-solutions/` — `cloud solutions`, 100% of 258 occurrences
- `/business-consulting/` — `business consulting`, 100% of 258 occurrences
- `/ai-machine-learning/` — `ai machine learning`, 100% of 258 occurrences
- `/project/pioneering-progress-exploring-the-evolution-and-impact-of/` — its long title anchor, 93.3% of 15 occurrences
- `/project/unlocking-potential-explore-our-comprehensive-it-portfolio/` — its long title anchor, 93.3% of 15 occurrences

The four hub warnings are largely expected from repeated navigation labels. Do not rewrite menu labels merely to manufacture anchor diversity. The anti-spam rule applies mainly to contextual body links, where the recommendation manifest deliberately varies language.

## Recommendation source

Use `docs/internal-link-recommendations.csv` as the implementation manifest. Every row contains Source URL, Target URL, Suggested natural anchor/context, Reason, Priority, and Action.

`ADD` rows can be implemented where surrounding copy supports them. `HOLD_FOR_CONSOLIDATION` and `HOLD_UNTIL_HOME_FIXED` rows must be resolved before strengthening those URLs.

## Important blockers before broad HTML insertion

1. `index.html` currently identifies itself as `Business Consulting – Techco`. The homepage and `/business-consulting/` must be made distinct before duplicating a homepage/consulting internal-link graph.
2. `/service/best-ui-ux-design-services/` and `/service/ui-ux-design-services/` overlap in intent. Pick one primary URL/canonical target before building authority to both.
3. Template/demo and legacy navigation should be cleaned before expanding internal links. The goal is fewer, stronger, contextually justified links—not a larger global link list.
