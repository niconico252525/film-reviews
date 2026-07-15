## Context

The initial data model supports movies, users, reviews, and calculated average
ratings. The project currently routes only Django admin, so none of that data
is available through public application pages. Exercise 6 calls for basic view
functions and explicit API documentation; the views may remain visually simple
but should establish stable URL names and response semantics.

## Goals / Non-Goals

**Goals:**

- Provide one clear function-based view per basic user action.
- Make the site navigable from home to list, detail, login, and review form.
- Support title filtering through a `q` query parameter.
- Validate review input and redirect after successful submission.
- Keep request handling in views and reusable query/write logic in services.
- Test successful responses, redirects, validation, authentication, and 404s.

**Non-Goals:**

- Production styling, pagination, sorting controls, or advanced search.
- Account registration, password customization, or profile pages.
- Review deletion, moderation, or revision history.
- JavaScript interactions or a JSON REST API.

## Decisions

### Use namespaced function-based routes

Create `reviews/urls.py` with `app_name = "reviews"` and include it at the
project root. Named routes make redirects and templates resilient to later path
changes while keeping each view as a plain callable.

### Render server-side templates

Views return Django `TemplateResponse`-style `HttpResponse` objects through
`render()`. A shared base template supplies navigation and messages. The HTML
is intentionally minimal because this exercise defines behavior, not final
visual design.

### Combine listing and search

`movie_list` accepts an optional GET parameter named `q`. The movie query
service returns all movies when it is blank and case-insensitive title matches
when provided. One route therefore supports both browsing and the first search
action without duplicating pages.

### Keep lookup failures explicit

Movie detail and review form views use `get_object_or_404`, returning HTTP 404
for unknown integer identifiers rather than an empty page or server error.

### Require authentication for review writes

The review view uses `login_required`. GET renders a form populated from an
existing review, if present. POST validates a 1–5 rating and non-empty body,
then calls a service that creates or updates the current user's one allowed
review for the movie. Success uses the POST/Redirect/GET pattern and returns an
HTTP redirect to movie detail.

### Reuse Django authentication URLs

Include Django's built-in authentication URL configuration at `/accounts/` and
provide a minimal login template. Account registration remains a later
feature.

## Risks / Trade-offs

- The list is unpaginated and may become slow with a large catalog; pagination
  can be added without changing its route.
- Review create and update share one action. This matches the unique
  author/movie constraint but does not expose review history.
- Templates are intentionally sparse and will need accessibility and design
  work before production use.
- The admin average display still performs per-row aggregation; public detail
  performs only one aggregate query and is acceptable for this increment.

## Migration Plan

No database migration is required. Deploy the URL, view, form, service, and
template changes together, then verify all named routes and tests. Rollback
removes the project URL includes and added files without changing stored data.

## Open Questions

None for this exercise. Registration and final visual design remain separate
backlog features.
