import json
import os
import stat
import subprocess
import sys
from pathlib import Path

from app import settings

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PRODUCTION_ENV_KEYS = {
    "DATABASE_URL",
    "DJANGO_ALLOWED_HOSTS",
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    "DJANGO_DEBUG",
    "RENDER",
    "RENDER_EXTERNAL_HOSTNAME",
    "SECRET_KEY",
}


def load_settings(extra_environment=None):
    environment = os.environ.copy()
    for key in PRODUCTION_ENV_KEYS:
        environment.pop(key, None)
    environment.update(extra_environment or {})

    script = """
import json
from app import settings

print(json.dumps({
    "allowed_hosts": settings.ALLOWED_HOSTS,
    "csrf_cookie_secure": settings.CSRF_COOKIE_SECURE,
    "csrf_trusted_origins": settings.CSRF_TRUSTED_ORIGINS,
    "database": settings.DATABASES["default"],
    "debug": settings.DEBUG,
    "hsts_seconds": settings.SECURE_HSTS_SECONDS,
    "middleware": settings.MIDDLEWARE,
    "proxy_header": settings.SECURE_PROXY_SSL_HEADER,
    "secure_redirect": settings.SECURE_SSL_REDIRECT,
    "session_cookie_secure": settings.SESSION_COOKIE_SECURE,
    "static_backend": settings.STORAGES["staticfiles"]["BACKEND"],
    "static_root": str(settings.STATIC_ROOT),
}, default=str))
"""
    return subprocess.run(
        [sys.executable, "-c", script],
        cwd=PROJECT_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )


def test_development_defaults_use_sqlite_and_local_hosts():
    result = load_settings()

    assert result.returncode == 0, result.stderr
    loaded = json.loads(result.stdout)
    assert loaded["debug"] is True
    assert loaded["database"]["ENGINE"] == "django.db.backends.sqlite3"
    assert loaded["allowed_hosts"] == ["127.0.0.1", "localhost", "[::1]"]
    assert loaded["secure_redirect"] is False


def test_production_requires_a_secret_key():
    result = load_settings(
        {
            "DJANGO_DEBUG": "false",
            "DJANGO_ALLOWED_HOSTS": "film-reviews.example.com",
        }
    )

    assert result.returncode != 0
    assert "Set SECRET_KEY before starting in production mode." in result.stderr


def test_production_requires_an_allowed_host():
    result = load_settings(
        {
            "DJANGO_DEBUG": "false",
            "SECRET_KEY": "production-secret-" + "x" * 60,
        }
    )

    assert result.returncode != 0
    assert "Set DJANGO_ALLOWED_HOSTS or RENDER_EXTERNAL_HOSTNAME" in result.stderr


def test_render_hostname_enables_production_security_and_csrf_origin():
    result = load_settings(
        {
            "RENDER": "true",
            "RENDER_EXTERNAL_HOSTNAME": "film-reviews.onrender.com",
            "SECRET_KEY": "production-secret-" + "x" * 60,
        }
    )

    assert result.returncode == 0, result.stderr
    loaded = json.loads(result.stdout)
    assert loaded["debug"] is False
    assert loaded["allowed_hosts"] == ["film-reviews.onrender.com"]
    assert loaded["csrf_trusted_origins"] == ["https://film-reviews.onrender.com"]
    assert loaded["proxy_header"] == ["HTTP_X_FORWARDED_PROTO", "https"]
    assert loaded["secure_redirect"] is True
    assert loaded["session_cookie_secure"] is True
    assert loaded["csrf_cookie_secure"] is True
    assert loaded["hsts_seconds"] == 31_536_000
    assert loaded["middleware"][:2] == [
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
    ]
    assert (
        loaded["static_backend"]
        == "whitenoise.storage.CompressedManifestStaticFilesStorage"
    )


def test_production_database_url_configures_postgresql_with_tls():
    result = load_settings(
        {
            "DATABASE_URL": "postgresql://film:secret@db.internal:5432/film_reviews",
            "DJANGO_ALLOWED_HOSTS": "film-reviews.example.com",
            "DJANGO_DEBUG": "false",
            "SECRET_KEY": "production-secret-" + "x" * 60,
        }
    )

    assert result.returncode == 0, result.stderr
    database = json.loads(result.stdout)["database"]
    assert database["ENGINE"] == "django.db.backends.postgresql"
    assert database["HOST"] == "db.internal"
    assert database["NAME"] == "film_reviews"
    assert database["CONN_MAX_AGE"] == 600
    assert database["OPTIONS"]["sslmode"] == "require"


def test_development_uses_unmanifested_static_storage():
    assert "whitenoise.middleware.WhiteNoiseMiddleware" not in settings.MIDDLEWARE
    assert (
        settings.STORAGES["staticfiles"]["BACKEND"]
        == "django.contrib.staticfiles.storage.StaticFilesStorage"
    )
    assert settings.STATIC_ROOT == PROJECT_ROOT / "staticfiles"


def test_render_blueprint_and_build_script_define_release_process():
    blueprint = (PROJECT_ROOT / "render.yaml").read_text()
    build_script_path = PROJECT_ROOT / "build.sh"
    build_script = build_script_path.read_text()

    assert "runtime: python" in blueprint
    assert "startCommand: gunicorn app.wsgi:application" in blueprint
    assert "healthCheckPath: /" in blueprint
    assert "generateValue: true" in blueprint
    assert "property: connectionString" in blueprint
    assert "ipAllowList: []" in blueprint
    assert "requirements-production.txt" in build_script
    assert "python manage.py collectstatic --no-input" in build_script
    assert "python manage.py check --deploy" in build_script
    assert "python manage.py migrate --no-input" in build_script
    assert build_script_path.stat().st_mode & stat.S_IXUSR
