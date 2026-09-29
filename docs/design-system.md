# Forsk Technologies Design System

This document defines the reusable visual system for Forsk Technologies without changing the website's established structural identity.

## Source of truth

Use this priority order when making visual decisions:

1. Current Forsk Technologies homepage.
2. Official blue / black / green Forsk Technologies logo family in `assets/images/logo/`.
3. Existing Techco / Bootstrap components and layout patterns that already work.
4. Legacy template defaults only when they do not conflict with the homepage or brand.

Do not introduce a new visual identity, unrelated accent colors, or decorative gradients.

## Brand palette

| Token | Value | Primary use |
| --- | --- | --- |
| `--brand-primary` | `#0044EB` | Main brand blue, primary actions, links, focus states |
| `--brand-primary-deep` | `#003796` | Hover states, stronger blue emphasis |
| `--brand-primary-soft` | `#EAF1FF` | Light blue badges and low-emphasis brand surfaces |
| `--brand-secondary` | `#020842` | Dark navy structural color, dark sections, strong headings |
| `--brand-accent` | `#47B16A` | Controlled green accent, positive actions/status |
| `--brand-accent-deep` | `#378C53` | Green hover/emphasis |
| `--text-primary` | `#131923` | Primary body/headline text where near-black is preferred |
| `--text-secondary` | `#49515B` | Body copy |
| `--text-muted` | `#6E7783` | Supporting text, captions, placeholders |
| `--page-background` | `#FFFFFF` | Page background |
| `--surface` | `#FFFFFF` | Cards/forms/components |
| `--surface-alt` | `#F1F6FC` | Alternate homepage-style section background |
| `--surface-dark` | `#020842` | Dark technology-oriented sections |
| `--border` | `#E3F0FF` | Standard subtle borders |
| `--border-strong` | `#CCE3FF` | Form controls and stronger separators |
| `--success` | `#47B16A` | Success feedback |
| `--error` | `#F26F4D` | Error/destructive feedback |
| `--warning` | `#F3A338` | Warnings |
| `--info` | `#23BABF` | Informational feedback |

### Color rules

- Blue is the main interactive brand color.
- Dark navy / near-black anchors typography and dark surfaces.
- Green is a controlled accent, not a second competing primary color.
- Do not use the old pink/purple template accent as a new site-wide brand color.
- Do not add new hex colors directly to new components when an existing token covers the requirement.
- If a gradient is necessary for an existing component, keep it inside the blue family. Prefer flat fills for new UI.

## Typography

The existing Axiforma family is retained.

- Body: `Axiforma Regular`
- Medium emphasis: `Axiforma Medium`
- UI / buttons: `Axiforma SemiBold`
- Headings: `Axiforma Bold`

Heading scale is deliberately close to the current homepage/theme instead of introducing a new oversized editorial scale:

- H1: responsive, maximum `54px`
- H2: responsive, maximum `45px`
- H3: responsive, maximum `32px`
- H4: `22px`
- H5: `18px`
- H6: `16px`
- Body base: `16px`
- Body line height: `1.625`
- Heading line height: `1.18`

Use strong size/weight hierarchy before adding decorative color.

## Spacing

The token system uses a 4px base rhythm:

`4, 8, 12, 16, 24, 32, 40, 48, 64, 80, 96, 120px`

Section spacing preserves the homepage's generous desktop rhythm:

- Desktop: `120px` vertical
- Large tablet / small desktop: `96px`
- Tablet: `80px`
- Mobile: `64px`

Avoid one-off padding values when the spacing scale can be used.

## Border radius

- Small: `8px`
- Medium: `10px`
- Large: `16px`
- Extra large / homepage card language: `20px`
- Pill: `999px`

Use `20px` for substantial cards/panels that visually align with the homepage. Use pill radius for CTA buttons and badges.

## Shadows

Shadows use dark navy at low opacity instead of neutral black-heavy effects:

- `--shadow-xs`: almost-flat separation
- `--shadow-sm`: standard floating card
- `--shadow-md`: interactive/elevated card
- `--shadow-focus`: accessible blue focus ring

Avoid large, blurry or colored glow effects.

## Buttons

Reusable classes:

- `.forsk-btn`
- `.forsk-btn--primary`
- `.forsk-btn--accent`
- `.forsk-btn--outline`

Button standards:

- Minimum height: `52px`
- Pill shape
- Axiforma SemiBold
- Restrained `translateY(-2px)` hover lift
- Primary: brand blue
- Accent: green only when an accent/positive CTA is justified
- Outline: neutral/navy base with blue hover

Existing `.btn-gradient` is retained for compatibility but its default gradient is constrained to brand blue -> deep blue rather than blue -> purple.

## Cards

Reusable classes:

- `.forsk-card`
- `.forsk-card--interactive`

Standard card:

- White surface
- `1px` light-blue border
- `20px` radius
- Low shadow by default
- Interactive cards can lift by `4px` and gain a slightly stronger shadow

Do not add multiple card styles for the same content type.

## Forms

Form controls use:

- White surface
- Strong border token
- `10px` radius
- `52px` minimum height for single-line controls
- Blue focus border/ring
- Green success border
- Coral-red error border
- Muted placeholders

Reusable optional class: `.forsk-field`.

## Badges

Reusable classes:

- `.forsk-badge`
- `.forsk-badge--accent`

Default badges use soft blue. Accent badges use soft green. Avoid rainbow badge systems unless a semantic state explicitly requires another semantic token.

## Links and interaction states

- Default content links: brand blue
- Hover: deep blue
- Keyboard focus: visible blue outline with offset
- Do not remove focus outlines without an accessible replacement
- Motion should be subtle and short; respect `prefers-reduced-motion`

## Section surfaces

Reusable classes:

- `.forsk-section`
- `.forsk-section--alt`
- `.forsk-section--dark`
- `.forsk-surface`
- `.forsk-surface-alt`

Alternate sections should normally use `#F1F6FC`, matching the homepage direction. Dark sections use the brand navy and white typography.

## Compatibility strategy

`assets/css/forsk-design-system.css` provides the design tokens and reusable classes while also mapping them to the existing Bootstrap/Techco variables.

`assets/css/inline-style.css` imports the design-system layer through a stylesheet that is already part of the current page CSS stack. This avoids changing page markup or the existing website structure.

The system also maps the generic Elementor kit variables to the Forsk palette using a higher-specificity compatibility selector. Existing page-specific styles can continue to override these where intentionally designed.

## Migration rules for future page work

1. Preserve the current URL, page hierarchy and section structure unless there is a separate approved structural task.
2. Reuse existing homepage patterns before creating a new component.
3. Use design tokens instead of hard-coded colors for new or edited UI.
4. Use Axiforma and the shared type scale.
5. Use the shared spacing/radius/shadow scales.
6. Prefer flat brand colors; do not introduce unrelated gradients.
7. Keep green selective so primary blue remains visually dominant.
8. Do not overwrite intentionally branded artwork or logo files with CSS effects.
9. When converting repeated markup to PHP includes later, keep these same component classes/tokens so visuals remain stable.
10. Test desktop, tablet and mobile after migrating any legacy component.
