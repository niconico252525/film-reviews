## ADDED Requirements

### Requirement: Shared semantic page structure

Every public HTML page MUST use the shared base template and expose a page
title, labeled primary navigation, one main landmark, and a footer. The shared
template MUST load presentation from an external static CSS file and MUST NOT
contain inline style declarations.

#### Scenario: Render a public page

- **WHEN** a visitor opens any public application page
- **THEN** the response contains the shared header, navigation, main content, footer, and stylesheet reference

### Requirement: Responsive presentation

The interface MUST use fluid layouts and responsive CSS so content, navigation,
forms, cards, and actions fit narrow and wide viewports without requiring
horizontal page scrolling. Text and controls MUST remain readable and usable at
mobile widths.

#### Scenario: Use a narrow viewport

- **WHEN** the stylesheet is applied at a viewport below its desktop breakpoint
- **THEN** multi-column and horizontal interface groups collapse into layouts that fit the available width

### Requirement: Accessible navigation and feedback

The interface MUST provide a keyboard skip link, visible focus indicators,
semantic labels, a current-page navigation indicator, live status messages,
and accessible form error summaries linked to invalid fields. Non-essential
transitions MUST respect reduced-motion preferences.

#### Scenario: Navigate by keyboard

- **WHEN** a keyboard user enters a page and focuses the skip link
- **THEN** the link becomes visible and moves focus navigation to the main content target

#### Scenario: Submit invalid form input

- **WHEN** a form response contains validation errors
- **THEN** the page renders an alert summary with links to the invalid fields and retains field-level error text

#### Scenario: Prefer reduced motion

- **WHEN** the user agent reports `prefers-reduced-motion: reduce`
- **THEN** the stylesheet disables non-essential transitions and smooth movement
