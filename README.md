# Techco â€” standalone HTML website

Public links continue to use the existing `.html` URLs. Repeated verified site chrome is now served through PHP includes, so converted pages require a PHP-capable Apache/LiteSpeed host with rewrite support. No WordPress installation, database, npm install, or build step is needed.

## Included

- 128 HTML pages, including the five homepage designs, service and project detail pages, blog posts and archives.
- Local CSS, JavaScript, images, icons and fonts. Existing visual styling and attribution are preserved.
- Local page search, mobile navigation, pricing switches, sliders and galleries.
- Keyboard support for mobile menu controls and search; reduced-motion CSS and visible focus indicators.

## Forms and external content

Contact, newsletter and comment forms download the entered information as a text file. They do **not** send email, post comments or subscribe visitors. Connect your chosen form backend before accepting live enquiries or subscriptions. Replace the template's demo contact information and promotional claims before using it for your business.

The Google map and YouTube links need an internet connection. Everything required for the page layouts is stored locally.

## Repairs

Recovered missing pages, images and generated styles from the original public theme demo. Removed WordPress API, feed, editor and emoji scripts and metadata. Repaired internal URLs, a missing mobile-menu event argument, missing font references and invalid slider initialization. Removed an unavailable decorative icon. Search and forms now have standalone behavior.

The original source folder was left unchanged. This folder is the converted deliverable. Theme imagery and third-party library licensing remain with their original owners.

## Resource folders

- `assets/css/` — all stylesheets
- `assets/js/` — scripts and local search index
- `assets/images/` — images, SVG icons and cursors
- `assets/fonts/` — local fonts

All pages use relative links to these folders, so the website also works in a subfolder and opens directly from disk.

## HTML pages

All 128 HTML pages are in the website root. The main page is `index.html`; other pages use descriptive names such as `about.html`, `contact.html`, `services.html`, `blog-page-2.html` and `service-it-management-services.html`. Date archives use `archive-` prefixes. See `page-map.json` for the complete old-to-new filename mapping. Resources remain in `assets/`.


## PHP includes

See `docs/php-architecture.md` for the conservative conversion scope, URL-preservation rules, skipped components, and validation details.
