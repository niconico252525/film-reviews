# AGENTS.md

## Project scope

Film Reviews is a Django web application for browsing movies and submitting reviews.

## Project stage

This is an **early-stage** project. Only the base Django configuration (`app/`)
exists — no custom Django apps (movies, reviews, accounts, etc.) have been
created yet. Models, views, services, forms, templates, and migrations all
need to be built.

Main features:

* Browse movies
* Search movies by title
* View movie details and ratings
* Create user accounts
* Submit reviews and ratings
* View reviews written by other users

## Important project conventions

* Put business logic in `services.py`, not in views.
* Keep views focused on request handling.
* Use models for data storage and relationships.
* Keep code simple and easy to understand.

## Environment

* Python >= 3.9
* Virtual env: `.venv/` (use `uv` to manage)
* Install: `uv sync` or `uv pip install -r requirements.txt`
* Activate: `source .venv/bin/activate`

## Commands

| Action | Command |
|--------|---------|
| Run server | `python manage.py runserver` |
| Run tests | `pytest` |
| Create migrations | `python manage.py makemigrations` |
| Apply migrations | `python manage.py migrate` |
| Lint | `ruff check .` |
| Format | `ruff format .` |
| Typecheck / Check | `python manage.py check` |
| Shell | `python manage.py shell` |

## Things that are easy to break

* Movie rating calculations
* User authentication
* Review submission logic
* Search and filtering functionality

## Change coupling

If you change:

* a model → also check views, forms, services, and tests
* review logic → also check rating calculations
* authentication → also check permissions and review creation

## Constraints

* Do not edit old migrations; create new migrations instead.
* If migration conflicts arise, use `python manage.py makemigrations --merge`.
* Keep changes small and focused.
* Follow Django best practices.

## Configuration

* `opencode.json` — project-level configuration for the opencode tool (lint,
  format, typecheck, test commands, and custom instructions).
* `AGENTS.md` (this file) — conventions and operating instructions for AI agents.
* `pyproject.toml` — Python tool configuration (ruff, pytest).
* Keep all three in sync when adding or changing commands.

## Documentation

* Keep documentation updated when features change.
* Report inconsistencies between code and documentation.

## Testing expectations

Add or update tests for:

* Review creation
* Rating calculations
* Search functionality
* User authentication

Tests live in `tests/` and mirror the `app/` structure.
