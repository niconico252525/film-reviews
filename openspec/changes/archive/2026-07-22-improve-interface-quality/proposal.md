## Why

Film Reviews is functional but relies almost entirely on browser-default
presentation. The pages need a consistent visual system, responsive behavior,
and accessible navigation and feedback before the interface can serve users
comfortably across devices and input methods.

## What Changes

- Add a reusable external stylesheet for layout, typography, color, forms,
  buttons, cards, messages, and responsive behavior.
- Refine the shared template into clear header, navigation, main, and footer
  landmarks with a keyboard-accessible skip link.
- Replace template-specific and inline presentation with reusable CSS classes.
- Improve page hierarchy and reusable layouts for home, movies, reviews, login,
  registration, and review editing.
- Add an accessible shared form-field and error-summary template.
- Add interface regression tests and document the design and accessibility
  behavior.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `web-interface`: Require a responsive, consistent, and accessible
  server-rendered page structure.

## Impact

The change updates templates, adds a static CSS file and interface tests, and
extends the web-interface specification and README. It does not change URLs,
database models, migrations, dependencies, or business behavior.
