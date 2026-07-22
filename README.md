# Film Reviews

## Project Description

Film Reviews is a Django web application where users can browse movies, read
reviews, create accounts, and submit their own reviews. The current runnable
increment provides the project configuration, SQLite schema, migrations,
Django admin integration, validated forms, and tested rating aggregation.

## Development Environment

- Python 3.9 or newer
- uv
- Git
- VS Code

## Tools

- Ruff (linter and formatter)
- Pytest (testing)
- Pytest-Cov (coverage)
- HTMX 2.0.10 (server-rendered partial updates)

## Setup

```bash
uv venv
source .venv/bin/activate
uv sync
python manage.py migrate
python manage.py runserver
```

The site is served at <http://127.0.0.1:8000/>. The first available interface
is Django admin at <http://127.0.0.1:8000/admin/>. Create an administrator with:

```bash
python manage.py createsuperuser
```

SQLite stores local data in the ignored `db.sqlite3` file.

## Database Design

The `reviews` app owns the initial domain schema:

| Model | Important fields | Rules |
| --- | --- | --- |
| `Movie` | title, optional release date, synopsis, timestamps | Title is indexed but not unique. |
| `Review` | movie, author, rating, body, timestamps | Rating is 1–5; one review is allowed per author/movie pair. |

`Review.author` uses Django's configured user model. Both the author and movie
relationships use cascading deletes. A movie's average rating is calculated
from its current reviews in `reviews/services.py`; it is not duplicated in the
database, so it cannot become stale. Both models provide human-readable
`__str__()` values and are registered in Django admin.

The normative design and behavior specification lives in
`openspec/specs/data-model/spec.md` after the completed OpenSpec change is
archived. The archived proposal and design retain the decision history.

## Web Interface API

All application responses are server-rendered HTML. URL names use the
`reviews` namespace, for example `reviews:movie_detail`.

| Method and path | Callable | Arguments | Return value |
| --- | --- | --- | --- |
| `GET /` | `reviews.views.home` | None | HTTP 200 using `reviews/home.html`; context contains up to five `recent_movies`. |
| `GET /movies/` | `reviews.views.movie_list` | Optional query argument `q` (string); optional request header `HX-Request: true` | A normal request returns HTTP 200 using `reviews/movie_list.html`. An HTMX request returns only `reviews/partials/movie_results.html`. Both contain the same validated, case-insensitive partial-title matches and vary on `HX-Request`. |
| `GET /accounts/register/` | `reviews.views.register_account` | None | Anonymous users receive HTTP 200 using `registration/register.html`. Authenticated users receive HTTP 302 to home. |
| `POST /accounts/register/` | `reviews.views.register_account` | Form `username`, required `email`, `password1`, and `password2` | Valid input creates and signs in the user, then returns HTTP 302 to home. Invalid input returns HTTP 200 with field errors and creates no user. |
| `GET /movies/<movie_id>/` | `reviews.views.movie_detail` | `movie_id` (integer primary key) | HTTP 200 using `reviews/movie_detail.html` with `movie`, `average_rating`, and `reviews`; HTTP 404 when the movie does not exist. |
| `GET /movies/<movie_id>/reviews/new/` | `reviews.views.review_create` | `movie_id` (integer primary key) | Authenticated users receive HTTP 200 using `reviews/review_form.html`; an existing review supplies the initial rating and body. Anonymous users receive HTTP 302 to `/accounts/login/` with a `next` argument. Unknown movies return HTTP 404 after authentication. |
| `POST /movies/<movie_id>/reviews/new/` | `reviews.views.review_create` | Path `movie_id`; form `rating` (integer 1–5) and `body` (non-empty string) | Valid input creates or updates the signed-in user's review and returns HTTP 302 to movie detail. Invalid input returns HTTP 200 with form errors and does not write a review. |

Supporting framework routes are `/accounts/login/` (`GET` form and `POST`
authentication), `/accounts/logout/` (`POST`, redirecting home), and `/admin/`.
After login, Django honors a valid `next` argument or redirects to `/`.

### Forms and User Input

| Form | Method | Fields and validation | Successful submission | Invalid submission |
| --- | --- | --- | --- | --- |
| Movie search | GET | Optional `q`; whitespace is stripped and length is limited to 255 characters. | Renders matching movies at the same bookmarkable URL. | Renders field errors and no results; no database write occurs. |
| Account registration | POST | Unique valid username, required valid email, and two matching passwords that pass Django's configured password validators. | Creates the user, starts an authenticated session, adds a success message, and redirects home. | Preserves non-password input, renders field errors, and creates no user. |
| Review create/update | POST | Rating must be one of 1–5; body must contain non-whitespace text. | Creates or updates the signed-in user's review, adds a success message, and redirects to movie detail. | Preserves submitted input, renders field errors, and writes no review. |

POST forms use CSRF protection and the POST/Redirect/GET pattern. GET is used
only for movie search because it is read-only and should remain bookmarkable.
All form pages extend `reviews/base.html`; the shared layout supplies
navigation, authentication actions, messages, and the main content region.

Profile pages, pagination, advanced search, email verification, and richer
branding remain future features. The current behavioral contract lives in
`openspec/specs/web-interface/spec.md`; archived OpenSpec changes retain the
decision history.

## Interface Design

All public pages extend `reviews/base.html`. The shared template provides the
site header, labeled navigation, live message region, one main landmark, and
footer. Repeated form fields and linked error summaries are rendered through a
shared include so login, registration, search, and review pages expose
consistent labels and feedback.

Presentation lives in `reviews/static/reviews/styles.css`. The stylesheet uses
system fonts, reusable color and spacing tokens, fluid containers, card and
surface components, and mobile-first layouts. Breakpoints at 38, 48, and 64
rem progressively enhance form actions, navigation, movie details, and card
grids without changing the HTML structure.

Accessibility features include:

- a keyboard skip link targeting the main content;
- high-contrast `:focus-visible` indicators and minimum-size controls;
- `aria-current` on the active navigation destination;
- semantic headings, lists, articles, landmarks, and `time` elements;
- live status messages and alert error summaries linked to invalid fields;
- form help and error text connected with `aria-describedby`;
- a reduced-motion media query that removes non-essential transitions.

The interface uses no external fonts, CSS frameworks, or image requests. HTMX
2.0.10 is loaded from jsDelivr with a pinned version and subresource integrity
hash. Search remains fully functional through normal GET submission when that
script is unavailable.

## HTMX Interaction

The movie list provides the first dynamic interaction while keeping the server
responsible for validation, filtering, and HTML rendering:

| Question | Design |
| --- | --- |
| What updates dynamically? | Matching movie cards and their result summary. |
| What triggers the update? | Changed search input after a 350ms pause, the native search event, or form submission. |
| Which page region changes? | Only the contents of `#movie-results`; navigation, the search field, and the rest of the document remain in place. |
| What does the browser request? | `GET /movies/?q=<title>` with `HX-Request: true`. The current query is pushed into browser history. |
| What does the server return? | `reviews/partials/movie_results.html`, containing the result heading, count, movie cards, empty state, or validation feedback. |
| What happens during a request? | The newest query replaces an older in-flight search and an accessible “Updating results…” indicator is revealed. |
| What is the fallback? | The same form performs a normal GET and receives the complete page when HTMX is unavailable. |

The response includes `Vary: HX-Request` so caches keep full documents and
partial fragments separate. No JSON endpoint or duplicate search logic is
introduced.

## Quality Checks

```bash
pytest
ruff check .
ruff format --check .
python manage.py check
python manage.py makemigrations --check
```
