# Forsk Technologies Mobile QA Audit

Date: 2026-09-29
Branch: `qa/mobile-responsive-audit-2026-09-29`
Scope: shared responsive behavior across the standalone HTML site, preserving the existing Forsk/Techco design system.

## Representative viewport matrix

| Category | Widths reviewed | Responsive expectation after fixes |
| --- | --- | --- |
| Small phones | 320px, 360px | Single-column content, full-width drawer, compact headings, no page-level horizontal scroll |
| Standard smartphones | 375px, 390px | Mobile navigation, 16px form inputs, 44px+ interactive targets, wrapped CTAs |
| Large phones | 430px | Mobile navigation, stable card/form spacing, contained media |
| Tablets | 768px, 1024px | Mobile navigation through 1199px, full-width generated wrappers, contained project cards |
| Laptops | 1366px | Desktop navigation with reduced menu spacing and existing visual hierarchy |
| Desktop | 1440px+ | Existing desktop navigation and design system retained |

## Findings and fixes

### HIGH — Header/navigation breakpoint conflict

**Problem:** Header markup uses `navbar-expand-xl`, but the desktop menu wrapper becomes visible at Bootstrap `lg` (992px). The hamburger behavior was effectively aligned to 991px, leaving 992–1199px vulnerable to crowded or overlapping navigation.

**Fix:** Desktop navigation is now hidden below 1200px and the existing mobile drawer is used through 1199px. The desktop menu returns at 1200px. No separate mobile site or duplicate navigation architecture was introduced.

### HIGH — Mobile touch targets too small

**Problem:** Mobile submenu toggles were 28×28px and close controls were roughly 36×36px, which is unnecessarily difficult to tap on phones.

**Fix:** Navigation toggles, close controls, primary buttons, accordion controls, filter buttons, pricing toggles and submit actions now use at least a 44px interaction height. Mobile submenu links reserve space for the larger toggle.

### HIGH — Mobile drawer viewport handling

**Problem:** The drawer used a fixed 300px width and `100vh`. On very small phones and modern mobile browser UI states this can produce awkward sizing and background scrolling.

**Fix:** Drawer width is bounded by the viewport, uses `100dvh` with a `100vh` fallback, accounts for safe-area insets, remains internally scrollable and locks document scrolling while open.

### HIGH — Horizontal overflow risks

**Problem:** Several generated/theme components depend on fixed widths, negative margins, long strings or intrinsic media sizing. A notable example is the project-card layout with large negative horizontal margins.

**Fix:** Shared layout wrappers can shrink correctly, media is constrained to its container, long text can wrap, project-card negative margins are removed below 1200px, sticky headers are constrained to the viewport and page-level horizontal overflow is clipped after correcting the main component sources.

### MEDIUM — Forms on phones

**Problem:** Some form controls can be smaller than comfortable touch size, and mobile browsers can zoom inputs when text is below 16px.

**Fix:** Phone form controls use at least 48px height and 16px text; textareas retain a useful minimum height. Form/card horizontal padding is reduced at narrow widths without changing colors, radius or component styling.

### MEDIUM — Wide tables

**Problem:** Tables can force the document wider than the viewport.

**Fix:** On phones, tables scroll inside their own region instead of creating page-level horizontal overflow. Existing `.table-responsive`, `.table-scroll` and `.wp-block-table` wrappers also get momentum scrolling.

### MEDIUM — 1366px laptop navigation density

**Problem:** The default desktop menu uses generous 48px gaps and a padded header, which can become crowded on common laptop widths.

**Fix:** Between 1200px and 1399.98px the existing desktop navigation keeps the same design but uses 24px menu spacing, smaller header-inner horizontal padding and the existing 14px navigation type size.

### MEDIUM — Footer and contact wrapping

**Problem:** Long footer/contact strings and generated row gutters can become cramped on phones.

**Fix:** Footer columns use tighter phone gutters and long links/addresses are allowed to wrap. Direct-contact groups use phone-appropriate gaps and vertical spacing.

### LOW — Sticky/back-to-top safe area

**Problem:** Fixed controls can sit too close to device edges/notches.

**Fix:** The existing back-to-top control now respects the right safe-area inset. Sticky header clones are prevented from exceeding viewport width.

## Component QA status

- Header: fixed breakpoint and narrow-width sizing.
- Navigation: fixed tablet transition, drawer sizing, scrolling and touch targets.
- Hero: existing responsive hero rules preserved; global shrink/wrap constraints prevent viewport escape.
- Cards: narrow padding and project-card overflow risk corrected.
- Typography: responsive wrapping preserved; extra small-phone heading safeguards added.
- Images/media: constrained to parent width; no logo artwork altered.
- Forms: phone sizing/touch behavior improved.
- Buttons: primary interactive controls meet a 44px minimum target.
- Tables: localized horizontal scrolling on phones.
- Footer: phone gutters and wrapping improved.
- Horizontal overflow: shared shrink constraints plus targeted fixes applied.
- Spacing: existing design tokens retained; only responsive spacing adjusted.
- Sticky elements: viewport and safe-area constraints added.

## Files changed

- `assets/css/mobile-qa.css` — cross-site responsive QA layer.
- `assets/css/static.css` — loads the QA layer after the theme styles.
- `docs/mobile-qa-audit-2026-09-29.md` — this audit record.

## Validation note

This pass validates the repository's shared responsive source and fixes the identified breakpoint/layout risks across representative widths. The connected desktop browser agent was offline during this run, so no claim is made that screenshot-based, physical-device or deployed-live visual regression testing was performed. A final visual smoke test should be run after the branch is deployed or previewed; the source-level fixes are isolated in `mobile-qa.css` for easy regression review.
