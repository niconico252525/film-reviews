## 1. Partial response layer

- [x] 1.1 Extract movie results into a reusable partial template.
- [x] 1.2 Return the partial for `HX-Request` and the full page otherwise.
- [x] 1.3 Add `Vary: HX-Request` to keep cached representations separate.

## 2. HTMX interaction

- [x] 2.1 Load the pinned HTMX script with integrity metadata.
- [x] 2.2 Add debounced input, result targeting, request synchronization, and URL history attributes.
- [x] 2.3 Add accessible progress and live-result states with project CSS.

## 3. Documentation and verification

- [x] 3.1 Document the trigger, target, request, response, fallback, and dependency.
- [x] 3.2 Add tests for full responses, partial responses, filtering, validation, caching, and markup.
- [x] 3.3 Run pytest, Django checks, migration checks, Ruff, and strict OpenSpec validation.
- [x] 3.4 Review the final interaction, archive OpenSpec, and complete the GitHub PR workflow.
