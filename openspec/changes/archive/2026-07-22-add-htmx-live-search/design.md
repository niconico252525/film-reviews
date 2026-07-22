## Context

`GET /movies/` already accepts a validated `q` argument and renders filtered
movies. The complete page and results markup are coupled in one template, so a
search submission reloads the shared header, navigation, form, and footer even
though only the result set changes.

## Goals / Non-Goals

**Goals:**

- Update matching movies after a short pause in typing without a full reload.
- Keep the server authoritative by returning rendered HTML rather than JSON.
- Reuse the existing URL, form validation, and search service.
- Make search URLs bookmarkable and browser-history aware.
- Expose progress and updated results to assistive technology.
- Preserve a complete-page GET fallback when HTMX is unavailable.
- Prevent stale in-flight searches from replacing newer results.

**Non-Goals:**

- Client-side filtering, autocomplete suggestions, fuzzy search, or advanced
  filters.
- Infinite scrolling, pagination, WebSockets, or JSON endpoints.
- Dynamic review submission or other HTMX interactions in this exercise.
- Changes to movies, reviews, authentication, or database schema.

## Decisions

### Use the existing movie-list endpoint

The search form sends HTMX GET requests to `/movies/` with the same `q` value
used by normal requests. The view checks the standard `HX-Request` header and
selects either the results partial or full template. This avoids duplicate URL
and search logic.

### Vary responses by HTMX request header

The view adds `Vary: HX-Request` so caches do not serve a partial response to a
normal navigation or a complete document to an HTMX swap.

### Debounce and synchronize active search

The form listens for changed input with a 350ms delay, native search events,
and form submission. `hx-sync="this:replace"` ensures the newest search replaces
an older in-flight request. `hx-target` and an inner HTML swap limit changes to
the results region.

### Preserve navigation and fallback behavior

`hx-push-url="true"` records the query in browser history. The form retains its
normal GET `action` and submit button, so failure to load HTMX falls back to a
complete server-rendered response with identical results.

### Keep progress and results perceivable

An `aria-live` results region announces updated content. A text indicator is
revealed while requests are active using project CSS, and reduced-motion rules
continue to apply. HTMX's built-in indicator styles are disabled to avoid
runtime inline CSS.

### Pin the browser dependency

The base template loads HTMX 2.0.10 from jsDelivr with the integrity hash and
anonymous cross-origin mode shown by the official installation documentation.
If the CDN is unavailable, normal form submission remains functional.

## Risks / Trade-offs

- The first interaction depends on a CDN when enhanced behavior is desired;
  the complete GET fallback prevents loss of search functionality.
- Each settled query performs a server request. Debouncing and request
  replacement reduce unnecessary work, while the existing indexed title field
  supports the simple filter.
- Template tests verify response boundaries and attributes but do not replace
  cross-browser interaction testing.

## Migration Plan

No database migration is required. Deploy the base template, movie template,
partial, view, CSS, tests, and documentation together. Rollback removes HTMX
attributes and returns the result markup to the full template; stored data is
unchanged.

## Open Questions

None for this exercise. Additional dynamic interactions should be separate
changes with their own fallback behavior.
