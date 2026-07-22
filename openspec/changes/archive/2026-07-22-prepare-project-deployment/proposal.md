## Why

The application currently assumes Django's development server, a checked-in
development secret, SQLite, and uncollected static assets. Those defaults are
appropriate for local development but do not provide a reproducible, secure,
or persistent production deployment.

## What Changes

- Add environment-driven production security, host, database, and proxy
  settings while preserving simple SQLite development.
- Run the WSGI application with Gunicorn on Render's assigned port.
- Collect versioned static assets and serve them through WhiteNoise.
- Define a Render Blueprint for a Python web service and private Render
  PostgreSQL database.
- Add a repeatable build script that installs locked dependencies, collects
  static files, checks deployment settings, and applies migrations.
- Document initial deployment, verification, operations, rollback, and the
  strategy for future user-uploaded files.
- Test the production settings contract without requiring a live database.

## Capabilities

### New Capabilities

- `deployment`: Define a reproducible and secure production deployment for the
  application.

### Modified Capabilities

None.

## Impact

The change updates project settings and dependencies, adds Render
infrastructure and build files, extends project documentation, and adds
configuration tests. It does not change application URLs, domain models, or
database migrations.
