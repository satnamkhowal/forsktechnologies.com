# Forsk Technologies Logo Audit and Usage Standard

Repository logo directory: `assets/images/logo/`

> Note: the requested `/image/logo/` path does not exist in the current repository. The official variants are stored in `assets/images/logo/`.

## Canonical usage

| Placement | Recommended asset | Rule |
|---|---|---|
| Main header on current white navigation surface | `forsk-technologies-horizontal-logo-blue-black-green-ai-agi-white-background.png` | Horizontal mark; constrain by max-height, never force width + height together. |
| Sticky header | `forsk-technologies-horizontal-logo-blue-black-green-ai-agi-white-background.png` | Existing sticky surface is white; use a smaller max-height. |
| Mobile navigation/header | `forsk-technologies-horizontal-logo-blue-black-green-ai-agi-white-background.png` | Same identity as desktop with smaller responsive bounds. |
| Light background outside header | `forsk-technologies-logo-blue-black-green-ai-agi-transparent-background.png` | Preferred where a transparent canvas is needed. |
| Dark background | `forsk-technologies-logo-white-green-ai-agi-dark-background.png` | Primary high-contrast dark-surface variant. |
| Footer on dark surface | `forsk-technologies-logo-white-green-ai-agi-dark-background.png` | Keep contained; do not stretch to fill footer columns. |
| Browser favicon | `forsk-technologies-favicon-blue-green.png` | Canonical favicon filename. |
| Social/avatar fallback | `forsk-technologies-square-logo-blue-black-green-ai-agi-white-background.png` | Suitable as a square brand/avatar fallback. Do not stretch it into 1200×630; use a dedicated social card when needed. |

## Exact duplicate files

The following pairs have identical Git blob SHAs, so they are byte-for-byte duplicates and should not both be referenced in new code:

- `forsk technologies Logo for for white horizontal background.png` = `forsk-technologies-horizontal-logo-blue-black-green-ai-agi-white-background.png`
- `forsk technologies Logo for white background.png` = `forsk-technologies-square-logo-blue-black-green-ai-agi-white-background.png`
- `forsk-technologies-fav-blue and green.png` = `forsk-technologies-favicon-blue-green.png`
- `Groot-Logo (2).jpg` = `forsk-technologies-logo-blue-black-green-learn-build-innovate-white-background.jpg`

Keep the descriptive, normalized `forsk-technologies-*` filenames as canonical references. The duplicate aliases can remain temporarily for backward compatibility until all references are confirmed migrated.

## Variant review

### Preferred active variants

- `forsk-technologies-horizontal-logo-blue-black-green-ai-agi-white-background.png` — primary horizontal light-surface/header logo.
- `forsk-technologies-logo-blue-black-green-ai-agi-transparent-background.png` — transparent light-surface/general-purpose logo.
- `forsk-technologies-logo-white-green-ai-agi-dark-background.png` — primary dark-surface logo.
- `forsk-technologies-square-logo-blue-black-green-ai-agi-white-background.png` — square/avatar/social fallback.
- `forsk-technologies-favicon-blue-green.png` — canonical browser favicon.

### Secondary / legacy variants

- `forsk-technologies-logo-red-white-ai-agi-dark-background.png` — alternate color treatment; do not use as the default brand mark.
- `forsk-technologies-logo-white-green-ai-agi-dark-background-alt.png` — alternate dark variant; reserve unless a specific layout requires it.
- `forsk-technologies-favicon-red-white.png`, `forsk-technologies-favicon-white-green.png`, `forsk-technologies-fav-red.png`, `forsk-technologies-fav-white-green.png` — theme-specific alternates, not the default browser icon.
- `Forsk Technologies-logo-for-dark-back-ground.png`, `forsk technologies Logo for dark background.png`, `forsk-technologies-logo-for-dark-background.png`, `forsk-logo.png` — large/ambiguously named assets; avoid new runtime references until a visual/source-file cleanup pass confirms a unique need.
- `forsk-technologies-logo-blue-black-green-learn-build-innovate-white-background.jpg` — tagline/marketing treatment; not suitable for compact header navigation.

## Implementation findings

- The current exported header uses `assets/images/site_logo_3-1.svg`, a theme logo rather than an official Forsk Technologies asset.
- The theme CSS previously constrained header logos primarily by `max-width: 124px`; it did not establish a consistent max-height across desktop, sticky, and mobile states.
- The current Header 3 navigation surface is white and the sticky menu also uses a white background, so the canonical blue/black/green horizontal variant is the correct default there.
- The stylesheet already keeps ordinary images at `height: auto`; the added brand rules reinforce `width: auto`, `height: auto`, `object-fit: contain`, responsive max-width, and max-height boundaries to prevent distortion.

## Sizing standard

- Desktop header: max 180px wide / 42px high.
- Sticky header: max 36px high.
- Tablet/mobile: max 150px wide / 34px high.
- Small mobile: max 138px wide / 32px high.
- Footer utility: max 200px wide / 52px high.

These are bounding boxes, not forced dimensions. The browser must preserve each image's intrinsic aspect ratio.

## Whitespace, dimensions, transparency and crop policy

Do not crop, rescale non-proportionally, recolor, trace, or recreate official artwork in CSS. If a source asset contains excessive internal canvas whitespace, fix the source only after visual confirmation and keep the visible artwork unchanged. Prefer transparent variants when the surrounding surface is not pure white. Avoid JPEG variants in navigation where transparent PNG artwork is available.

The runtime implementation intentionally avoids deleting legacy files because some static exported pages may still reference older aliases. Remove aliases only after a repository-wide reference migration is complete.
