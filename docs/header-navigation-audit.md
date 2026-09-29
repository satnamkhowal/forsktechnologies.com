# Forsk Technologies Header & Navigation Audit

## Scope

The homepage header is the visual reference. Existing navigation destinations and hierarchy are preserved. The implementation is improved through the already shared `assets/css/static.css` and `assets/js/static.js` layers so the same behavior applies to every exported page that loads those files.

## Findings and fixes

| Area | Finding | Improvement |
| --- | --- | --- |
| Official logo | Header and mobile drawer still referenced the old theme `site_logo_3-1.svg`. | Header and mobile navigation now use the official transparent Forsk Technologies logo from `assets/images/logo/`, with consistent max dimensions and meaningful alt text. |
| Desktop navigation | Theme dropdown behavior was primarily mouse-hover driven. | Existing visual dropdowns are retained, with focus-within support, ARIA state, Arrow Down entry, Escape close, and Left/Right/Home/End movement across top-level items. |
| Mobile navigation | Theme generated submenu controls as non-semantic spans. | Existing controls are enhanced with keyboard activation, `role=button`, focusability, labels, `aria-controls`, and `aria-expanded`. |
| Active state | Static WordPress-export classes can identify the wrong page. | Active item and parent state are recalculated from the current URL at runtime and `aria-current=page` is applied to matching links. |
| Sticky header | Theme clones the full header for sticky behavior, duplicating element IDs and exposing two copies to assistive technology. | IDs in the sticky clone are made unique; only the currently visible original/sticky header is exposed to the accessibility tree and focus order. |
| Responsive breakpoint | Desktop menu wrapper became visible at Bootstrap `lg` (992px) while the layout declares `navbar-expand-xl` (1200px). | 992-1199px now deliberately uses the mobile/off-canvas navigation, avoiding cramped/overflowing desktop navigation. |
| Touch targets | Menu toggle/close/submenu controls were smaller or inconsistent. | Mobile controls and navigation rows use at least 44-48px targets. |
| CTA | Existing `Get Started` CTA is retained. | Target sizing and no-wrap behavior are normalized; on narrow phones the secondary header CTA is hidden to prevent collision while Contact remains available in navigation. |
| Overflow | Large mega menus and the off-canvas drawer could exceed narrow viewports. | Drawer width/height, scroll containment, mega-menu max width, and horizontal overflow safeguards are standardized. |
| Focus handling | Mobile drawer had no focus containment or reliable focus return. | Opening moves focus into the drawer, Tab cycles inside while open, Escape closes, and focus returns to the menu trigger. |

## Architecture decision

A PHP header include is **not introduced in this isolated change**. The repository is currently a static `.html` export and has no existing PHP page architecture. Converting only the header to `include()` would either require changing page extensions/URLs or configuring the server to execute `.html` as PHP, both of which would create deployment and URL risk outside this task.

The current shared CSS/JS files are already loaded site-wide, so they are the safest central layer for consistent logo, navigation state, accessibility, responsive behavior, sticky behavior, and overflow fixes without changing the existing page URLs or visible structure.

When the broader PHP conversion is undertaken, the current header markup can be moved into a single `includes/header.php` after URL-preservation/rewrite behavior is tested as a separate architecture migration.

## Regression checklist

- Desktop: 1200px, 1366px, 1440px, 1920px
- Tablet/mobile-nav breakpoint: 992px, 1024px, 1199px
- Mobile: 320px, 375px, 390px, 430px, 768px
- Keyboard: Tab, Shift+Tab, Enter/Space on mobile toggles, Arrow Down on desktop dropdown parent, Arrow Left/Right, Home/End, Escape
- Sticky transition before/after 150px scroll
- Active state on Home, About/Company child, Portfolio, Services/service child, Blog/blog detail, Contact
- Mobile drawer scrolling with long mega-menu content
- No horizontal viewport overflow
- Official logo remains proportional and sharp in original, sticky, and mobile header states
