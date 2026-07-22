## Why

Movie search currently reloads the complete page for every submission. Search
results are a focused region that can be refreshed independently, making them
a suitable first server-driven interaction while preserving the existing URL
and query service.

## What Changes

- Add HTMX 2.0.10 to the shared page template with a pinned version and
  subresource integrity metadata.
- Trigger a debounced movie search while the title field changes.
- Replace only the results region and update browser history with the current
  query URL.
- Return a results partial for HTMX requests and the complete movie-list page
  for normal requests.
- Add an accessible in-progress indicator and retain normal form submission as
  a no-script fallback.
- Document and test the full-page and partial-response contracts.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `web-interface`: Add a progressively enhanced live movie search interaction.

## Impact

The change updates the movie-list view and template, adds one reusable partial,
loads the HTMX browser library, extends CSS and documentation, and adds request
tests. It introduces no database migration, Python dependency, new URL, or
business-logic change.
