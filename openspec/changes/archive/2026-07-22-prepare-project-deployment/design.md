## Context

Film Reviews is a synchronous Django 4.2 WSGI application. Local development
uses SQLite and Django's static-file development behavior. A production host
needs persistent relational storage, TLS-aware security settings, collected
static assets, a process manager, and a repeatable deployment definition.

## Goals / Non-Goals

**Goals:**

- Deploy the application to an internet-accessible Render web service.
- Keep secrets outside version control and fail clearly when production lacks
  a secret.
- Use managed PostgreSQL through `DATABASE_URL` in production.
- Serve fingerprinted, compressed static files without a separate web server.
- Run schema migrations and deployment checks on every build.
- Keep local setup compatible with SQLite and Python 3.9 or newer.
- Document verification, administration, rollback, and data/media behavior.

**Non-Goals:**

- Container orchestration, multiple application instances, background jobs, or
  a CDN.
- A custom domain, outbound email, monitoring integration, or automated
  database backups beyond the selected hosting plan.
- Adding file-upload or image fields to the application.
- Copying existing local SQLite data into production.

## Decisions

### Host the application and database on Render

A repository-level `render.yaml` Blueprint defines one Python web service and
one Render PostgreSQL database in the Singapore region. The service tracks
`main`, performs health checks against `/`, generates `SECRET_KEY_SEED`, and
receives the database's private connection string without storing credentials
in Git. Django expands the platform's 256-bit generated seed through SHA-512 so
the effective secret also satisfies Django's deployment length check.
The initial free plan is suitable for this exercise; production owners can
change plan sizes without changing application code.

### Use Gunicorn as the application server

Gunicorn runs `app.wsgi:application`, binds to Render's `PORT`, and writes
access and error logs to standard output. The application remains synchronous,
so adding an ASGI worker would add complexity without a current requirement.

### Select settings from explicit environment variables

Local development remains the default with debug enabled, the development
secret, localhost hosts, and SQLite. `DJANGO_DEBUG=false` activates production
security. Production requires `SECRET_KEY`; parses hosts and trusted origins
from environment variables; trusts Render's TLS proxy header; enables secure
cookies, HTTPS redirect, HSTS, content-type sniffing protection, and referrer
policy; and uses `DATABASE_URL` when provided.

The automatically provided `RENDER_EXTERNAL_HOSTNAME` is added to allowed hosts
and its HTTPS origin is trusted for CSRF. Optional comma-separated values allow
custom domains and local production-mode verification.

### Use PostgreSQL through dj-database-url and psycopg

`dj-database-url` parses Render's private PostgreSQL connection string and
enables persistent connections. `psycopg` supplies the database driver. When
`DATABASE_URL` is absent, development and tests retain the existing SQLite
database, avoiding a mandatory local PostgreSQL service.

### Serve static assets with WhiteNoise

`collectstatic` writes to `STATIC_ROOT`. WhiteNoise middleware sits immediately
after Django's security middleware and uses compressed manifest storage, which
gives content-hashed names, compression, and long-lived caching. This covers
project CSS and Django admin assets.

WhiteNoise is not used for user uploads. The current schema has no upload or
image fields. A future upload feature must use durable object storage such as
S3 or an equivalent service because Render web-service filesystems are
ephemeral and application-domain media serving is inappropriate for uploads.

### Keep migrations in the build for the free deployment

`build.sh` installs requirements, collects static assets, runs Django's
deployment check, and applies migrations. Render's separate pre-deploy command
is preferable for larger paid deployments but is unavailable to free web
services. Migrations therefore remain backwards-compatible and are applied
during the build before the new process starts.

### Pin a compatible Python series

`.python-version` selects Python 3.12 on Render because Django 4.2 does not
support Render's newer default Python series. Project metadata continues to
allow Python 3.9 and newer compatible interpreters for local development.

## Risks / Trade-offs

- Free web services can sleep and free PostgreSQL has lifecycle and capacity
  limits; a durable real deployment should select paid plans and backups.
- Running migrations in the build can affect the live database before a new
  release starts. Migrations must remain backwards-compatible; a paid service
  can move the same command to `preDeployCommand`.
- WhiteNoise keeps the deployment self-contained but is not a replacement for
  object storage or a CDN for user media and high traffic.
- HTTPS redirect depends on the hosting proxy sending the forwarded-protocol
  header. Render provides this header; another host must provide equivalent
  proxy behavior or adjust the setting.

## Migration Plan

1. Deploy the Blueprint from the merged `main` branch.
2. Render creates PostgreSQL, generates the secret, installs dependencies,
   collects assets, checks settings, and applies existing migrations.
3. Gunicorn starts and Render verifies `/` through its health check.
4. Verify the public home, movie list, static stylesheet, login, and admin
   routes over HTTPS.
5. Create a production administrator from a Render shell when needed.

Rollback uses Render's last successful deploy. Because this change contains no
schema migration, application rollback is safe. If a future release includes a
database change, use a forward corrective migration instead of reversing data
destructively.

## Open Questions

The final public URL is assigned when the Blueprint instance is created and
will be recorded in the README after deployment.
