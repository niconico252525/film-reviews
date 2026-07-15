## 1. Project and application setup

- [x] 1.1 Generate the `reviews` Django app with `manage.py startapp` and add the missing standard ASGI entry point.
- [x] 1.2 Register the app and align declared development dependencies and pytest configuration.

## 2. Database implementation

- [x] 2.1 Implement `Movie` and `Review` models, relationships, constraints, ordering, and `__str__()` methods.
- [x] 2.2 Add the average-rating service and register both models with Django admin.
- [x] 2.3 Generate and apply the initial `reviews` migration to SQLite.

## 3. Verification

- [x] 3.1 Add model tests for strings, relationships, validation, uniqueness, database constraints, and cascade deletion.
- [x] 3.2 Add service tests for unrated and rated movies and admin registration tests.
- [x] 3.3 Run pytest, Django checks, migration consistency checks, and Ruff; refactor any findings.

## 4. Documentation and delivery

- [x] 4.1 Update the project README/specification with setup commands and the database design.
- [ ] 4.2 Verify the implementation against this change and archive it into the living OpenSpec specification.
- [ ] 4.3 Commit with the GitHub issue-closing keyword, open and review the pull request, then merge and clean up the feature branch.
