## 1. Production configuration

- [x] 1.1 Add environment-driven Django security, host, database, proxy, and static-file settings.
- [x] 1.2 Add Gunicorn, PostgreSQL, database URL, and WhiteNoise dependencies with a compatible Python version.
- [x] 1.3 Add a repeatable build script and Render Blueprint for the web service and database.

## 2. Documentation and tests

- [x] 2.1 Test development defaults, production requirements, Render host/origin handling, PostgreSQL parsing, and static storage.
- [x] 2.2 Document the hosting, application server, static and media strategy, environment variables, deployment workflow, verification, operations, and rollback.
- [x] 2.3 Update project operating documentation for the production stack and commands.

## 3. Verification and delivery

- [x] 3.1 Run unit tests, Django checks including `--deploy`, migration checks, Ruff, static collection, and strict OpenSpec validation.
- [x] 3.2 Start Gunicorn with production-mode settings and verify an HTTP response plus WhiteNoise static delivery.
- [ ] 3.3 Review the final change, archive OpenSpec, and complete the GitHub PR workflow.
- [ ] 3.4 Create the Render Blueprint instance, verify the public deployment, and record its URL.
