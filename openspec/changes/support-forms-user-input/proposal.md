## Why

Film Reviews accepts review and search values, but search input bypasses Django
form validation and visitors cannot create the user account required to submit
reviews. Exercise 8 requires a clear, validated input contract instead of raw
or hard-coded values.

## What Changes

- Validate movie-title searches with a reusable GET form.
- Add a registration form for username, email, and confirmed password input.
- Add a registration action that creates and signs in a valid user.
- Keep review validation explicit and continue persisting reviews through the
  service layer.
- Render validation errors and submitted values in shared Django templates.
- Document each form's method, fields, validation, success response, and error
  response.
- Add form, service, and request tests for valid and invalid submissions.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `web-interface`: Define validated GET and POST forms for search,
  registration, and review submission.

## Impact

The change updates forms, views, services, URLs, templates, tests, and user
input documentation. It uses Django's configured user model and password
validators. No database migration or dependency change is required.
