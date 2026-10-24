# Forsk Technologies practical accessibility audit

Date: 2026-09-29

Scope reviewed: shared theme CSS/JS plus representative homepage, contact and portfolio markup. Goal: improve keyboard, screen-reader and touch usability without redesigning the site or adding ARIA where native HTML already supplies correct semantics.

## Findings

| Priority | Area | Finding | Remediation |
| --- | --- | --- | --- |
| HIGH | Semantic HTML | Main page content uses `#elementor_page_builder` rather than a `main` landmark and there is no skip link. | Shared layer exposes the wrapper as the main landmark and adds a keyboard-visible skip link. Long-term: change the wrapper to a real `<main>`. |
| HIGH | Keyboard navigation | Desktop dropdowns are hover-driven. | Added `:focus-within` behavior so submenu links are reachable by keyboard. |
| HIGH | Mobile navigation | `.xb-menu-close` and generated `.xb-menu-toggle` are non-native pseudo-controls. | Keyboard fallback, state synchronization, focus entry and Escape/Close focus restoration are added. Long-term: generate real `<button type="button">` elements. |
| HIGH | Focus states | Theme reset removes outlines from links, inputs, textareas and buttons. | Added a two-tone visible `:focus-visible` indicator that remains detectable on light and dark surfaces. |
| HIGH | Forms / labels | Contact fields have correct visible labels, but placeholder-style `aria-label` values override them; `aria-required` duplicates native `required`; static `aria-invalid="false"` can become stale. | Redundant ARIA is removed when a real label exists; `aria-invalid="true"` is set only after an actual validation failure and removed when valid. |
| HIGH | Touch targets | Mobile submenu toggles are styled at 28×28px. | Menu toggle/open/close targets are raised to at least 44×44px on mobile. |
| MEDIUM | Footer form | Newsletter label is empty and relies on placeholder/ARIA. | A visually-hidden label is populated and remains associated with the existing input. |
| MEDIUM | Link names / alt | Linked logo images have empty `alt`; back-to-top is an unnamed icon-only link. | Linked logos receive native alt text and the back-to-top link receives an accessible name. Decorative image `alt=""` values are otherwise preserved. |
| MEDIUM | Heading structure | Main content generally uses H1 then H2 sections, but mega-menu category labels use H3 before the page H1 in DOM order. | Source follow-up: use styled non-heading text for menu labels unless they genuinely introduce document subsections. |
| MEDIUM | Contrast | White on success green `#47B16A` is about 2.70:1; white on secondary pink `#F44380` is about 3.52:1. Both fail 4.5:1 for normal text. | Verified affected combinations use existing dark navy text instead. Primary blue + white, body text + white and dark navy + white already have strong contrast. |
| MEDIUM | Motion | CSS honors `prefers-reduced-motion`, but Swiper autoplay can continue. | Swiper autoplay is stopped when reduced motion is requested. |
| LOW | Search dialog | Generated `<dialog>` had a visible H2 but no explicit accessible name. | Added `aria-labelledby` pointing to the dialog heading. |

## Native HTML / ARIA policy

Do not add `role="button"` to real buttons, `role="link"` to anchors with valid `href`, or duplicate visible labels with `aria-label`. Use ARIA only for state/relationships native HTML does not provide, such as `aria-expanded`, `aria-controls`, or an icon-only control's accessible name.

The remaining `.xb-menu-close` / `.xb-menu-toggle` role-and-tabindex handling is a compatibility fallback, not the preferred final markup.

## Alt-text policy

Do not blanket-fill every empty `alt`. Keep `alt=""` for decorative quotes, shapes and duplicated visuals. Add concise alt text only when an image contributes information or is the sole accessible content of a link/control.

## Remaining source-level work

1. Replace `#elementor_page_builder` div with a real `<main>` in generated page markup, then remove the runtime `role="main"` fallback.
2. Convert `.xb-menu-close` and generated `.xb-menu-toggle` to native buttons while preserving existing classes and visual styling.
3. Replace mega-menu H3 labels used only for styling with non-heading elements.
4. Continue contextual page-by-page review of content-bearing images; do not mass-generate alt text.
5. If forms become server-backed, make server errors visible, programmatically associated and announced without unpredictable focus movement.

## Regression checklist

- Skip link appears on keyboard focus and moves focus to main content.
- Desktop dropdowns remain reachable with keyboard only.
- Mobile nav works with Enter/Space; Escape closes and restores focus.
- Focus indicator is visible on light and dark sections.
- Contact fields announce visible labels and only expose invalid state after a validation failure.
- Footer email input has an accessible name independent of placeholder text.
- Icon-only controls have accessible names.
- Mobile navigation targets are at least 44×44px.
- Reduced-motion preference stops autoplaying Swiper content.
- No blanket ARIA or blanket image-alt generation is introduced.
