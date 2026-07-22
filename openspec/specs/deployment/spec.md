# deployment Specification

## Purpose
TBD - created by archiving change prepare-project-deployment. Update Purpose after archive.
## Requirements
### Requirement: Environment-based production security

The application MUST disable debug output in production, MUST obtain its secret
key and permitted hosts from environment-specific values, MUST understand the
hosting proxy's HTTPS signal, and MUST enable secure transport and cookie
settings. Starting production without a non-development secret MUST fail.

#### Scenario: Start with complete production configuration

- **WHEN** the process starts with debug disabled, a production secret, and a permitted host
- **THEN** Django loads with debug disabled and HTTPS, secure-cookie, proxy, and host protections enabled

#### Scenario: Start without a production secret

- **WHEN** the process starts with debug disabled and no non-development secret
- **THEN** settings initialization fails with a configuration error before serving requests

### Requirement: Environment-selected persistent database

The application MUST use the PostgreSQL connection supplied by `DATABASE_URL`
when present and MUST retain SQLite as the default for local development and
tests. Production database connections MUST require TLS.

#### Scenario: Load a hosted database URL

- **WHEN** settings receive a PostgreSQL `DATABASE_URL` with debug disabled
- **THEN** Django configures the PostgreSQL backend with persistent connections and SSL required

#### Scenario: Develop without a database URL

- **WHEN** a developer starts the project without `DATABASE_URL`
- **THEN** Django uses the local ignored SQLite database

### Requirement: Production application and static servers

The deployed service MUST run the WSGI application with Gunicorn. A deployment
build MUST install declared dependencies, collect static files, validate
production settings, and apply database migrations. WhiteNoise MUST serve
compressed, content-versioned static assets collected under `STATIC_ROOT`.

#### Scenario: Build a release

- **WHEN** the hosting platform executes the repository build command
- **THEN** dependencies install, deployment checks pass, static assets are collected, and migrations are applied before Gunicorn starts

#### Scenario: Request a static asset

- **WHEN** a production client requests a collected project stylesheet
- **THEN** WhiteNoise returns the asset independently of Django's development static server

### Requirement: Reproducible Render infrastructure

The repository MUST define a Render Python web service and private PostgreSQL
database as a Blueprint. The service MUST receive a generated secret seed and
the database connection through environment variables, derive a Django secret
that passes deployment checks, use a compatible Python version, bind to the
assigned port, and expose an HTTP health-check path.

#### Scenario: Create a Blueprint instance

- **WHEN** an operator applies `render.yaml` to the repository's main branch
- **THEN** Render can create the linked database and web service without committing secret values

### Requirement: Durable uploaded-file policy

Project documentation MUST state whether uploads currently exist and MUST
define durable object storage as the required approach before upload or image
fields are introduced. Runtime-local files MUST NOT be treated as persistent
user media.

#### Scenario: Plan a future upload feature

- **WHEN** a developer reads the deployment documentation before adding uploads
- **THEN** they know that Render's ephemeral filesystem and WhiteNoise are not the media store and that external object storage is required

