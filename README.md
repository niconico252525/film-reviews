# Film Reviews

## Project Description

Film Reviews is a Django web application where users can browse movies, read
reviews, and submit their own reviews. This first runnable increment provides
the project configuration, SQLite schema, migrations, Django admin integration,
and tested rating aggregation on which the public features can be built.

## Development Environment

- Python 3.9 or newer
- uv
- Git
- VS Code

## Tools

- Ruff (linter and formatter)
- Pytest (testing)
- Pytest-Cov (coverage)

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
| `GET /movies/` | `reviews.views.movie_list` | Optional query argument `q` (string) | HTTP 200 using `reviews/movie_list.html`; context contains `movies` and the normalized `query`. A non-blank query performs case-insensitive partial-title matching. |
| `GET /movies/<movie_id>/` | `reviews.views.movie_detail` | `movie_id` (integer primary key) | HTTP 200 using `reviews/movie_detail.html` with `movie`, `average_rating`, and `reviews`; HTTP 404 when the movie does not exist. |
| `GET /movies/<movie_id>/reviews/new/` | `reviews.views.review_create` | `movie_id` (integer primary key) | Authenticated users receive HTTP 200 using `reviews/review_form.html`; an existing review supplies the initial rating and body. Anonymous users receive HTTP 302 to `/accounts/login/` with a `next` argument. Unknown movies return HTTP 404 after authentication. |
| `POST /movies/<movie_id>/reviews/new/` | `reviews.views.review_create` | Path `movie_id`; form `rating` (integer 1–5) and `body` (non-empty string) | Valid input creates or updates the signed-in user's review and returns HTTP 302 to movie detail. Invalid input returns HTTP 200 with form errors and does not write a review. |

Supporting framework routes are `/accounts/login/` (`GET` form and `POST`
authentication), `/accounts/logout/` (`POST`, redirecting home), and `/admin/`.
After login, Django honors a valid `next` argument or redirects to `/`.

Minimal templates are intentional for this exercise; public registration,
pagination, advanced search, and final styling remain future features. The
behavioral contract is recorded in the active OpenSpec capability
`openspec/changes/add-basic-views/specs/web-interface/spec.md`.

## Quality Checks

```bash
pytest
ruff check .
ruff format --check .
python manage.py check
python manage.py makemigrations --check
```
