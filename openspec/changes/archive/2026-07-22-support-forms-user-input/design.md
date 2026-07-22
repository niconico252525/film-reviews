## Context

The site already has a shared base template, a raw `q` search input, built-in
login/logout views, and an authenticated review form. Account registration is
the missing step in the core user journey, and search input currently has no
length validation or reusable form contract.

## Goals / Non-Goals

**Goals:**

- Use Django forms as the validation boundary for all current user input.
- Use GET for idempotent movie search and POST for registration and reviews.
- Validate search length, username uniqueness, email syntax, password policy
  and confirmation, rating range, and non-blank review text.
- Preserve submitted values and show field errors after invalid input.
- Keep persistence outside views and apply POST/Redirect/GET after success.
- Reuse the existing base template for every form page.

**Non-Goals:**

- Profile editing, password reset customization, social login, or email
  verification.
- Advanced search filters, pagination, autocomplete, or JavaScript forms.
- Review deletion, moderation, file uploads, or rich-text input.
- A custom user model or database-schema changes.

## Decisions

### Validate search with a GET form

`MovieSearchForm` exposes optional `q` text with a 255-character maximum. The
movie-list view binds `request.GET`, searches only when the form is valid, and
returns no matches with visible errors for invalid input. GET keeps searches
bookmarkable and safe to repeat.

### Reuse Django's account validation

`RegistrationForm` extends `UserCreationForm`, adds a required email field, and
therefore reuses username uniqueness, password confirmation, and configured
password validators. A registration service creates the user from validated
values. Successful registration signs the user in and redirects home.

### Keep review persistence in the service layer

`ReviewForm` remains the request-input boundary for a 1–5 rating and non-blank
body. The view passes cleaned values to `save_review`, which validates the
model and creates or updates the user's single review.

### Reuse the shared page structure

The registration page extends `reviews/base.html`; navigation links anonymous
visitors to both login and registration. Search and review forms continue to
render within the same layout, with CSRF tokens on POST forms.

## Risks / Trade-offs

- Requiring email improves the initial contact data but does not verify email
  ownership; verification remains future work.
- Automatically signing in after registration is convenient but assumes the
  default authentication backend; the service returns the created user so the
  view can pass it to Django's `login()`.
- Invalid oversized searches return no results instead of the full catalog so
  users cannot mistake rejected input for a successful broad search.

## Migration Plan

No database migration is required. Deploy forms, service, view, URL, template,
and documentation changes together. Rollback removes the registration route
and restores the raw search binding without altering existing users or reviews.

## Open Questions

Email verification and profile management remain backlog work.
