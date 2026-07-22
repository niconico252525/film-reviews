## Context

All public pages already extend one base template, which provides a useful
foundation for a design system. The current markup has only minimal landmarks,
uses an inline style for logout, renders raw form paragraphs, and has no static
stylesheet, responsive layout, skip navigation, or explicit focus treatment.

## Goals / Non-Goals

**Goals:**

- Establish a clean, reusable visual language without changing application
  behavior.
- Use semantic landmarks, ordered heading levels, lists, articles, and time
  elements where they communicate page structure.
- Support keyboard navigation, visible focus, skip navigation, status messages,
  error summaries, labels, help text, and reduced-motion preferences.
- Use mobile-first responsive CSS that avoids horizontal overflow and adapts
  navigation, cards, actions, and forms to narrow viewports.
- Keep presentation in a versioned static CSS file and remove inline styles.
- Test critical HTML and CSS accessibility contracts.

**Non-Goals:**

- JavaScript interactions, a CSS framework, custom fonts, icons, or image
  assets.
- Dark mode, user-selectable themes, animation-heavy effects, or a final brand
  identity.
- Changes to models, views, services, URLs, authentication behavior, or form
  validation rules.
- Automated browser screenshots or full WCAG certification.

## Decisions

### Use a small CSS design system

Add `reviews/static/reviews/styles.css` with design tokens, a content container,
surface and card components, button variants, form states, and responsive
utilities. System fonts and CSS-only decoration avoid new dependencies and
network requests.

### Keep templates semantic and reusable

The base template owns the site header, grouped navigation, status messages,
main landmark, and footer. Page templates use descriptive sections, articles,
lists, and actions. Repeated form field and error markup moves to one include.

### Design mobile first

The default layout fits narrow screens. Min-width media queries introduce
multi-column cards and horizontal action groups only when space is available.
Controls remain at least 44 pixels tall, text wraps, and containers use fluid
widths with bounded readable line lengths.

### Make interaction state perceivable

A skip link becomes visible on focus, all interactive elements receive a
high-contrast `:focus-visible` outline, current navigation uses
`aria-current`, messages use a live status region, and invalid forms expose a
linked error summary with field-level errors. Reduced-motion preferences
disable non-essential transitions.

## Risks / Trade-offs

- Template-level tests can verify structure but not visual rendering in every
  browser; CSS remains intentionally simple and standards-based.
- Rendering form fields manually adds markup but centralizes accessibility and
  prevents page-specific drift.
- The palette is deliberately restrained; later branding can replace design
  tokens without rewriting templates.

## Migration Plan

No database migration is required. Deploy static CSS and templates together so
pages never reference a missing stylesheet. Rollback restores the prior
templates and removes the static file without affecting stored data.

## Open Questions

None for this exercise. Dark mode and richer branding can be evaluated later.
