## Why

Film Reviews has a database schema and admin interface but no public pages or
application URLs. Users need a first navigable web interface that demonstrates
the core request/response actions before richer styling and account flows are
built.

## What Changes

- Add function-based views for the home page, movie listing/search, movie
  detail, and review creation or update.
- Add namespaced application URLs and connect them to the project URL
  configuration.
- Add minimal templates for navigation, movie display, review submission, and
  login.
- Keep movie queries and review persistence in services rather than views.
- Document every callable URL, accepted argument, and response behavior.
- Add request-level and service-level tests for the new behavior.

## Capabilities

### New Capabilities

- `web-interface`: Provide the first public request/response interface for
  browsing movies and submitting authenticated reviews.

### Modified Capabilities

None.

## Impact

The change adds URL routes, templates, a small review form, and view/service
tests. It uses Django's built-in authentication views and the existing Movie
and Review schema. No database migration or public account-registration flow is
introduced.
