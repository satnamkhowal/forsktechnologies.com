# Forsk Technologies Image Audit — 2026-09-29

Repository: `satnamkhowal/forsktechnologies.com`

Scope: repository image assets plus representative live-page markup patterns. Official logo artwork is treated as protected brand material: this audit does not recolor, redraw, crop, stretch, or otherwise alter logo identity.

## Executive summary

The repository already uses WebP for many primary content images, which is good. The largest remaining opportunities are not a blanket “convert everything” exercise; they are concentrated in oversized decorative/background assets, legacy JPEG/PNG blog/template assets, exact duplicate files, inconsistent filenames, and markup where alt/dimension/loading behavior is incomplete.

Confirmed findings:

- Multiple exact byte-for-byte duplicate image groups exist. The confirmed groups listed below contain about **1.21 MiB of redundant bytes** before checking whether every duplicate path is still referenced.
- Several decorative WebP assets are unusually heavy, including `bg_image_3.webp` (~529 KiB), `bg_image_2-scaled.webp` (~457 KiB), `circle_engine_2.webp` (~458 KiB), and `team_map-1024x950.webp` (~362 KiB).
- Several SVG decorations are very large for vector assets: `bg_pattern_1.svg` (~687 KiB), `bg_pattern_2.svg` (~798 KiB), `best_offer.svg.svg` (~443 KiB), and `fontawesome-webfont.svg` (~434 KiB).
- A legacy JPEG/PNG pool remains beside the WebP set. This includes `post_*.jpg`, `cs_blog_*.jpg`, `story_*.jpg`, `sc_feature_*.jpg`, `hero_Image.jpg`, `ml_hero_img.jpg`, `top_bg.jpg`, and many decorative PNGs.
- Some filenames are poor for maintainability/SEO, including spaces/case inconsistencies, `best_offer.svg.svg`, `cs_cirlce_shape.png`, `technlogies.png`, and `hero_Image.jpg`.
- The main/header logo SVG itself has intrinsic dimensions (`137×51`), so its artwork is not the problem. However, page markup should still use explicit image dimensions when the logo is rendered to reserve layout space consistently.
- Representative markup contains inherited template alt text on Forsk branding and empty alt text on some visible content images. Decorative images may intentionally use `alt=""`; content-bearing images should not.
- Many content images already have `loading="lazy"` and explicit dimensions. Those working patterns should be retained rather than globally changing every `<img>`.

## High-priority oversized assets

| Asset | Size | Finding | Recommended action |
|---|---:|---|---|
| `assets/images/bg_pattern_2.svg` | 816,811 B | Extremely large vector decoration | SVGO-style minification; simplify metadata/path data only if visually identical |
| `assets/images/bg_pattern_1.svg` | 703,554 B | Extremely large vector decoration | Minify/simplify without visual redesign |
| `assets/images/bg_image_3.webp` | 542,036 B | Heavy WebP background | Resize to actual rendered maximum; re-encode WebP and generate AVIF fallback candidate |
| `assets/images/circle_engine_2.webp` | 469,194 B | Heavy decorative raster | Confirm rendered size, resize, re-encode; likely strong savings |
| `assets/images/bg_image_2-scaled.webp` | 467,508 B | Heavy WebP background | Re-encode/resize to rendered need |
| `assets/images/best_offer.svg.svg` | 454,165 B | Heavy SVG + bad double extension | Minify; rename only after all references are updated |
| `assets/images/fontawesome-webfont.svg` | 444,379 B | Font asset stored in image directory | Confirm usage; prefer WOFF2 font source and remove only if unreferenced |
| `assets/images/team_map-1024x950.webp` | 371,124 B | Heavy map illustration | Re-encode/resize after checking display dimensions |
| `assets/images/bg_image_4.webp` | 348,290 B | Heavy WebP background | Re-encode/resize |
| `assets/images/shape_angle_1.webp` | 287,226 B | Heavy decorative raster | Resize/re-encode |
| `assets/images/post_10.jpg` | 254,578 B | Legacy JPEG with smaller derivative present | Prefer correctly sized derivative/WebP when used |
| `assets/images/post_09.jpg` | 209,323 B | Legacy JPEG with 800×600 derivative present | Prefer correctly sized derivative/WebP when used |
| `assets/images/testimonial_shape.png` | 205,491 B | Heavy decorative PNG | Convert to WebP/AVIF if transparency is required; otherwise optimize |
| `assets/images/service_details_image_5-1-scaled.webp` | 196,924 B | Heavy WebP | Resize/re-encode to actual rendered size |
| `assets/images/bg_image_1-scaled.webp` | 195,832 B | Heavy WebP background | Re-encode/resize |
| `assets/images/shape_angle_4-747x1024.webp` | 193,904 B | Large decorative asset | Check rendered size and downscale |
| `assets/images/post_04.jpg` | 193,434 B | Legacy JPEG; 800×600 derivative exists | Prefer derivative/WebP |
| `assets/images/cs_blog_02.jpg` | 189,794 B | Legacy JPEG; 600×350 derivative exists | Prefer derivative/WebP |
| `assets/images/post_06.jpg` | 185,885 B | Legacy JPEG | Convert to WebP/AVIF if referenced |
| `assets/images/cs_cirlce_shape.png` | 175,212 B | Heavy PNG + typo in name | Convert if referenced; rename only with reference migration |
| `assets/images/avatar_7*.webp` | 171,220 B each | Four byte-identical copies | Consolidate references before deleting duplicates |

## Official logo assets

Large logo-source files exist under `assets/images/logo/`, including PNGs around 0.7–0.85 MiB. These are **not candidates for destructive visual optimization** without a verified branding workflow. Safe actions are:

1. Keep the original artwork untouched as the brand master.
2. Use an existing SVG logo where appropriate for page chrome.
3. If raster logos must be served, create separate optimized derivatives at the exact display size while retaining originals.
4. Consolidate only exact duplicate copies after all references are migrated.
5. Do not recolor, redraw, crop, stretch, or change logo proportions.

Confirmed exact logo-file duplicates include:

- `forsk-technologies-fav-blue and green.png` = `forsk-technologies-favicon-blue-green.png`
- `forsk technologies Logo for for white horizontal background.png` = `forsk-technologies-horizontal-logo-blue-black-green-ai-agi-white-background.png`
- `Groot-Logo (2).jpg` = `forsk-technologies-logo-blue-black-green-learn-build-innovate-white-background.jpg`
- `forsk technologies Logo for white background.png` = `forsk-technologies-square-logo-blue-black-green-ai-agi-white-background.png`

These should be deduplicated only after reference checks.

## Confirmed duplicate asset groups

The files below share the same Git blob SHA, so they are byte-for-byte identical:

- `avatar_6.webp`, `avatar_6-1.webp`
- `avatar_7.webp`, `avatar_7-1.webp`, `avatar_7-2.webp`, `avatar_7-3.webp`
- `client_logo_8.webp`, `client_logo_8-1.webp`
- `client_logo_9.webp`, `client_logo_9-1.webp`
- `bg_pattern_3.svg`, `bg_pattern_3-1.svg`
- `shape_space_2.svg`, `shape_space_2-1.svg`
- `site_logo_2.svg`, `site_logo_2-3752b76b.svg`
- `site_logo_3-1-bd699173.svg`, `site_logo_3-2.svg`
- `cs_shape1.png`, `t_shape1.png`, `t_shape4.png`
- `cs_shape2.png`, `t_shape2.png`, `t_shape3.png`
- `avatar1.png`, `s_avatar3.png`
- the four official-logo duplicate pairs listed above

**Do not delete duplicate paths blindly.** The repository is currently not indexed by GitHub code search, so usage must be established by scanning the source files directly. Consolidate references to one canonical path first, then remove the redundant file.

## Legacy PNG/JPEG conversion queue

Prioritize referenced files rather than converting unused template debris. Strong candidates include:

- Blog/post imagery: `post_01.jpg` through `post_10.jpg`, `cs_blog_01.jpg` through `cs_blog_03.jpg`
- Story/feature imagery: `story_01.jpg`, `story_02.jpg`, `story_03.jpg`, `sc_feature_01.jpg`, `sc_feature_02.jpg`, `sc_feature_03.jpg`
- Hero/background imagery: `hero_Image.jpg`, `ml_hero_img.jpg`, `top_bg.jpg`, `business_consulting_hero_section_bg.jpg`
- Decorative PNGs above ~20 KiB: `blog_bg_shape.png`, `circle_engine_4.png`, `cta_bg_shape.png`, `cta_lbur.png`, `ft_blur.png`, `hero_bottom_shape-1.png`, `hero_image.png`, `ml_hero_shape*.png`, `sc_feature_bg.png`, `sc_service_bg.png`, `testimonial_shape.png`, `technlogies.png`, `cs_cirlce_shape.png`

Recommended serving strategy:

- Photos: generate WebP; AVIF can be added through `<picture>` where browser negotiation is worth the markup complexity.
- Transparent UI/decorative rasters: WebP is generally the first safe replacement; AVIF may also work but should be visually checked for sharp edges/transparency.
- Tiny PNGs (hundreds of bytes to a few KiB) often do not justify format migration.
- SVG icons should stay SVG and be minified rather than rasterized.

## Dimensions and CLS

The main logo SVG declares `width="137" height="51" viewBox="0 0 137 51"`, so the original vector has a stable intrinsic ratio. When used through `<img>`, mirror those dimensions in HTML unless CSS deliberately renders another known size.

For all content images:

- Add `width` and `height` matching the source aspect ratio.
- Keep responsive CSS such as `max-width:100%; height:auto`.
- Do not lazy-load the LCP/above-the-fold hero image.
- Use `loading="lazy"` on below-the-fold content images.
- Use `decoding="async"` for non-critical raster images.
- For the likely LCP image, use `fetchpriority="high"` only after confirming it is the actual LCP candidate.
- Background images that determine element height should have the container dimensions/aspect ratio defined in CSS; background images themselves do not support HTML width/height attributes.

## Alt text findings and rules

Representative pages show three categories that should be normalized:

1. **Brand logo:** use concise `alt="Forsk Technologies"` when the logo links to the home page and conveys site identity.
2. **Content image:** provide short, page-context-specific alternative text when the image conveys information.
3. **Pure decoration:** keep `alt=""` (and optionally `aria-hidden="true"`) so assistive technology skips it.

Do not turn every filename into keyword-stuffed alt text. Empty alt text is valid for decoration; it is only a defect when the image is meaningfully informational.

## Filename cleanup

Poor/inconsistent names found include:

- `best_offer.svg.svg` — double extension
- `cs_cirlce_shape.png` — typo
- `technlogies.png` — typo
- `hero_Image.jpg` — inconsistent capitalization
- logo files with spaces and mixed capitalization
- generated/hash suffix variants such as `site_logo_2-3752b76b.svg`

Rename only as part of a source-reference migration. A “prettier” filename is not worth breaking a working URL.

## Safe implementation order

### P0 — no visual risk

- Scan all source files for actual image usage.
- Add/repair missing semantic alt text on content images and Forsk branding.
- Add explicit width/height to `<img>` elements where intrinsic dimensions are known.
- Keep hero/LCP images eager; lazy-load only below-the-fold images.
- Identify exact duplicate paths that are truly unused after canonical-reference migration.

### P1 — high performance impact

- Resize/re-encode the heavy WebP backgrounds/decorations listed above.
- Minify the very large SVG backgrounds and icon/illustration files.
- Convert referenced legacy JPEG/PNG content images to WebP; add AVIF only where it materially reduces bytes.

### P2 — cleanup

- Consolidate old WordPress/generated image variants after usage verification.
- Rename poor filenames only when references can be updated atomically.
- Remove `dummy.png` and misplaced/legacy font-image assets only after proving they are unreferenced.

## Validation requirements after optimization

- Pixel/visual comparison for logos and brand marks.
- Broken-reference scan across HTML/CSS/JS.
- Confirm image aspect ratios and no stretched assets.
- Confirm no hero/LCP image was accidentally lazy-loaded.
- Confirm decorative alt text remains empty and content alt text is meaningful.
- Run Lighthouse/Web Vitals on representative home, service, about, portfolio, blog, and contact pages.
- Compare total transferred image bytes before/after.

## Important repository observation

`index.html` and `business-consulting.html` currently share the same Git blob SHA. That is broader than the image audit, but it means image-reference changes to one may need to be evaluated against the other rather than assumed to represent separate templates.
