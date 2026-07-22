## ADDED Requirements

### Requirement: HTMX live movie search

The movie-list search form SHALL progressively enhance title search with HTMX.
Changed input MUST trigger a debounced GET request, and the response MUST
replace only the movie-results region. The browser URL MUST reflect the current
query, newer input MUST replace an older in-flight search, and normal GET form
submission MUST remain functional without HTMX.

#### Scenario: Update matching movies while typing

- **WHEN** a visitor changes the search title and pauses for the configured debounce interval
- **THEN** the browser requests `/movies/` with the current `q` value and replaces only the results region with matching movies

#### Scenario: Use the no-script fallback

- **WHEN** HTMX is unavailable and a visitor submits the search form
- **THEN** the browser performs a normal GET navigation and receives the complete movie-list page with the same matching results

### Requirement: Movie search partial response

The server MUST return only reusable movie-results markup when `HX-Request` is
`true`, MUST return the complete HTML document otherwise, and MUST add
`HX-Request` to the response `Vary` header. Partial results and progress MUST be
exposed through accessible live status text.

#### Scenario: Request a search partial

- **WHEN** the server receives `GET /movies/?q=alien` with `HX-Request: true`
- **THEN** it returns the movie-results partial without the shared page document and varies the response on `HX-Request`

#### Scenario: Request a complete search page

- **WHEN** the server receives the same GET request without an HTMX header
- **THEN** it returns the complete movie-list document containing the search form and included results partial

#### Scenario: Search request is in progress

- **WHEN** an HTMX movie search is waiting for a server response
- **THEN** a text progress indicator becomes perceivable without moving keyboard focus
