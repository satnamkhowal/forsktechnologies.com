# Forsk Technologies practical accessibility audit

Date: 2026-09-29

Scope reviewed: shared theme CSS/JS plus representative homepage, contact and portfolio markup. The goal is practical accessibility improvement without redesigning the site or adding ARIA where native HTML already supplies the correct semantics.

## Summary

The site already had a small standalone accessibility layer, including `:focus-visible` and reduced-motion CSS. The audit found several important gaps in the inherited theme: missing main/skip navigation semantics, hover-dependent desktop dropdowns, pseudo-button mobile controls, 28x28 submenu touch targets, empty accessible names on some icon/logo links, redundant/stale form ARIA, and two verified low-contrast theme combinations.

The shared fixes in `assets/js/static.js` improve these behaviors across pages while preserving layout and styling. Source-level semantic cleanup is still recommended for the remaining pseudo-controls and heading structure.

## Findings and remediation

| Priority | Area | Finding | Action |
| --- | --- | --- | --- |
| HIGH | Semantic HTML | Page content is wrapped by `#elementor_page_builder` rather than a `main` landmark, and there is no skip link. | Shared layer now exposes the content as the main landmark and inserts a keyboard-visible “Skip to main content” link. Long-term source fix: change the wrapper to `<main id="elementor_page_builder">` rather than relying on `role="main"`. |
| HIGH | Keyboard navigation | Desktop dropdown CSS is hover-driven, so keyboard focus did not guarantee submenu visibility. | Added `:focus-within` behavior for desktop dropdowns so submenu links remain reachable by Tab. |
| HIGH | Mobile navigation | `.xb-menu-close` and generated `.xb-menu-toggle` controls are non-native elements repaired with `role="button"`/`tabindex`. | Existing keyboard fallback is retained and state is synchronized with `aria-expanded`/`aria-controls`; opening the mobile menu moves focus into it and Escape/Close restores focus. Long-term source fix: generate real `<button type="button">` controls. |
| HIGH | Focus states | Theme reset removes outlines from links, inputs, textareas and buttons. A later shared rule restored focus, but a single blue outline can lose visibility on dark/blue surfaces. | Added a two-tone white/blue focus indicator for keyboard focus. No mouse-only focus decoration is forced. |
| HIGH | Forms / labels | Contact inputs have correct visible `<label for>` associations, but redundant `aria-label` values containing placeholder examples override those visible labels. `aria-required="true"` duplicates native `required`, and static `aria-invalid="false"` can become stale. | Shared layer removes redundant ARIA when a real visible label exists, keeps native `required`, and sets `aria-invalid="true"` only after a real validation failure. |
| HIGH | Touch targets | Mobile submenu toggles are styled at 28x28px. | Shared mobile rule increases menu toggle/close/open targets to at least 44x44px. |
| MEDIUM | Form labels | Footer newsletter has an empty `<label>` and relies on placeholder/`aria-label`. | Shared layer supplies a visually-hidden label tied to the existing input. The icon-only submit button keeps an accessible name because it has no visible text. |
| MEDIUM | Link names / alt | Linked header/mobile logos use empty `alt`, producing an unnamed image link. The back-to-top link is also icon-only without a name. | Shared layer gives linked logos the native image alt text “Forsk Technologies” and names the back-to-top link. Decorative image `alt=""` is otherwise preserved intentionally. |
| MEDIUM | Heading structure | Main content generally has an H1 followed by H2 sections, but mega-menu content uses H3 headings before the page H1 in DOM order. | Source-level follow-up: use non-heading text for menu category labels unless they truly introduce document subsections. Do not change visual typography; style a `<span>`/`<p>` with the existing class. |
| MEDIUM | Contrast | Theme palette gives white on success green `#47B16A` about 2.70:1 and white on secondary pink `#F44380` about 3.52:1, both below 4.5:1 for normal text. The homepage includes white text on the success background, and secondary badges can inherit white text. | Shared layer uses the existing dark navy text on these verified combinations. Primary blue + white, body text + white, and dark navy + white already have strong contrast. |
| MEDIUM | Motion | CSS honors `prefers-reduced-motion`, but Swiper autoplay can continue changing slides. | Shared layer stops Swiper autoplay when reduced motion is requested. |
| LOW | Search dialog ARIA | The generated `<dialog>` had a visible H2 but no explicit accessible name. | Added `aria-labelledby` pointing to the generated heading. This ARIA is necessary because the native dialog element does not automatically take its accessible name from arbitrary descendant text. |

## Native HTML policy

Do not add `role="button"` to real `<button>` elements, do not add `role="link"` to anchors with valid `href`, and do not duplicate visible labels with `aria-label`. ARIA should represent state/relationships that native markup does not provide, such as `aria-expanded`, `aria-controls`, or the accessible name of an icon-only control.

The remaining non-native `.xb-menu-close` / `.xb-menu-toggle` controls should ultimately be converted in the source generator/theme JavaScript to real buttons. The current role/tabindex handling is a compatibility fallback, not the preferred final markup.

## Alt-text policy

Do not automatically fill every empty `alt`. Keep `alt=""` for decorative quotes, shapes, duplicated visual thumbnails, and imagery whose adjacent text already conveys the same information. Add concise alt text only when the image contributes information or is the sole accessible content of a link/control. Linked brand logos need a useful accessible name.

## Form-error policy

Use native constraints (`required`, `type="email"`, etc.) first. Browser `reportValidity()` is already used by the static form behavior. Only set `aria-invalid="true"` after a control actually fails validation, and remove it when the value becomes valid. If custom server-side errors are introduced later, render visible error text and connect it with `aria-describedby` to the relevant field.

## Remaining source-level work

1. Replace `#elementor_page_builder` div with a real `<main>` in page templates/exports, then remove the fallback `role="main"` injection.
2. Change `.xb-menu-close` and generated `.xb-menu-toggle` from div/span pseudo-controls to native buttons, preserving classes and visuals.
3. Replace mega-menu H3 category labels with styled non-heading text unless a heading is structurally justified.
4. Continue page-by-page review of content-bearing images; do not mass-generate alt text.
5. When forms become server-backed, ensure server validation errors are visible, programmatically associated, and announced without moving focus unpredictably.

## Regression checklist

- Tab from browser chrome: skip link appears and moves focus to main content.
- Desktop nav: every submenu can be opened/reached with keyboard only.
- Mobile nav: open button, close button and submenu toggles work with Enter/Space; Escape closes and returns focus.
- Focus indicator is visible on both light and dark sections.
- Contact fields announce visible labels, required state and invalid state correctly.
- Footer email input has a usable accessible name independent of placeholder text.
- Icon-only controls have accessible names.
- Touch targets for mobile navigation are at least 44x44px.
- Reduced-motion preference stops autoplaying Swiper content.
- No blanket ARIA or blanket image-alt generation is introduced.
