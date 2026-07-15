## Context

The repository contains Django project settings and an admin URL, but no
custom app or database domain model. The first schema must support the stated
movie-browsing and review use cases while remaining small enough to evolve in
an early-stage project. SQLite is already configured for development.

## Goals / Non-Goals

**Goals:**

- Persist movies and reviews with clear ownership and deletion behavior.
- Enforce important review invariants both in Python validation and in the
  database.
- Make records easy to identify in Django admin.
- Derive average ratings from current reviews rather than duplicating data.
- Provide a reproducible migration and automated database tests.

**Non-Goals:**

- Public browsing, search views, authentication screens, or review forms.
- A custom user model, genre taxonomy, poster uploads, or external movie data.
- Production database, deployment, or media-storage configuration.

## Decisions

### Use one domain app

Create a `reviews` app with `python manage.py startapp reviews`. `Movie` and
`Review` are closely related in this first increment, so splitting them would
add structure without a current boundary or independent behavior.

### Store movies without title uniqueness

`Movie` stores an indexed `title`, optional `release_date`, optional
`synopsis`, and audit timestamps. Titles are not unique because distinct films
can legitimately share a title. The title index supports later case-insensitive
searches.

### Relate reviews to the configured user model

`Review.author` references `settings.AUTH_USER_MODEL`, and `Review.movie`
references `Movie`. Both use `CASCADE`: deleting a user removes content that can
no longer have an author, and deleting a movie removes reviews that no longer
have a subject. Related names are `reviews` on both relationships.

### Enforce review invariants at two layers

Ratings use `PositiveSmallIntegerField` with `MinValueValidator(1)` and
`MaxValueValidator(5)` so forms and `full_clean()` return useful validation
errors. A database check constraint also prevents ratings outside 1–5 when
model validation is bypassed. A unique constraint on `(author, movie)` permits
one review per user per movie and supports a later edit-in-place workflow.

### Calculate rather than persist aggregate ratings

The average rating is returned by a small service using Django's `Avg`
aggregation. Storing the average on `Movie` would require synchronization on
every create, update, and delete and could become stale.

### Optimize admin identification

`Movie.__str__()` returns the title and release year when available.
`Review.__str__()` returns author, movie, and rating. Both models are registered
with list displays, search fields, filters, and sensible ordering.

## Risks / Trade-offs

- `CASCADE` removes reviews with their author. If the product later needs
  permanent reviews after account deletion, author anonymization will require a
  migration and policy change.
- One review per user/movie prevents review history. A separate revision model
  can be introduced if history becomes a requirement.
- SQLite check-constraint behavior is sufficient for development; production
  database compatibility must be verified when a production engine is chosen.
- The built-in user model keeps this increment small but makes a later custom
  user-model migration expensive. No custom identity fields are currently
  required.

## Migration Plan

1. Register `reviews.apps.ReviewsConfig` in `INSTALLED_APPS`.
2. Generate and inspect `reviews/migrations/0001_initial.py`.
3. Run all migrations against a fresh SQLite database.
4. Run model, service, and admin tests plus Django's system and migration
   consistency checks.

Rollback is safe before production data exists: reverse the `reviews` initial
migration, remove the app from `INSTALLED_APPS`, and remove the app code. Old
migrations will not be edited once committed.

## Open Questions

None for this increment. Genre modeling, poster storage, and custom user fields
remain deferred until their product requirements are defined.
