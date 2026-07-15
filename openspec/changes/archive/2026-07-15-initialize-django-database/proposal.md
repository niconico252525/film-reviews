## Why

Film Reviews has a base Django project but no domain application, database
schema, migrations, or model tests. A small, explicit schema is needed before
movie browsing and review-submission features can be built safely.

## What Changes

- Add a Django `reviews` application generated through `manage.py`.
- Add movie and review persistence using Django's configured SQLite database.
- Relate reviews to Django users and movies with database-enforced rating and
  uniqueness constraints.
- Register the domain models in Django admin with useful string
  representations.
- Add an initial migration and model/service/admin unit tests.
- Document the database design and runnable development workflow.

## Capabilities

### New Capabilities

- `data-model`: Persist movies and user-authored reviews, expose meaningful
  model labels in admin, and calculate current aggregate ratings.

### Modified Capabilities

None.

## Impact

The change adds a `reviews` Django app, new SQLite tables, a dependency on
`pytest-django` for database tests, an initial migration, and database setup
documentation. It uses Django's existing built-in authentication tables and
does not add public views, forms, or templates.
