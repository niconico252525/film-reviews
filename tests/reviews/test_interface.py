from datetime import date
from pathlib import Path

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from reviews.models import Movie, Review

pytestmark = pytest.mark.django_db

PROJECT_ROOT = Path(__file__).resolve().parents[2]
STYLESHEET_PATH = PROJECT_ROOT / "reviews" / "static" / "reviews" / "styles.css"


@pytest.mark.parametrize(
    "url_name",
    ["reviews:home", "reviews:movie_list", "login", "reviews:register"],
)
def test_public_pages_use_shared_semantic_layout_and_external_css(client, url_name):
    response = client.get(reverse(url_name))
    content = response.content.decode()

    assert response.status_code == 200
    assert '<link rel="stylesheet" href="/static/reviews/styles.css">' in content
    assert '<a class="skip-link" href="#main-content">' in content
    assert '<nav class="site-nav" aria-label="Main navigation">' in content
    assert '<main id="main-content"' in content
    assert '<footer class="site-footer">' in content
    assert "style=" not in content


def test_stylesheet_defines_responsive_and_accessible_interaction_rules():
    css = STYLESHEET_PATH.read_text()

    assert ":focus-visible" in css
    assert ".skip-link:focus" in css
    assert "@media (min-width: 38rem)" in css
    assert "@media (min-width: 48rem)" in css
    assert "@media (min-width: 64rem)" in css
    assert "@media (prefers-reduced-motion: reduce)" in css
    assert "overflow-wrap: anywhere" in css


def test_current_navigation_item_is_identified(client):
    response = client.get(reverse("reviews:movie_list"))

    assert b'href="/movies/" aria-current="page"' in response.content


def test_invalid_registration_links_error_summary_to_accessible_fields(client):
    get_user_model().objects.create_user(username="existing-reviewer")

    response = client.post(
        reverse("reviews:register"),
        {
            "username": "existing-reviewer",
            "email": "not-an-email",
            "password1": "X9!mQ2#vL7$p",
            "password2": "different-password",
        },
    )
    content = response.content.decode()

    assert response.status_code == 200
    assert 'class="form-error-summary" role="alert"' in content
    assert 'href="#id_username"' in content
    assert 'id="id_username_errors"' in content
    assert 'aria-invalid="true"' in content
    assert 'aria-describedby="id_username_helptext id_username_errors"' in content


def test_success_message_is_exposed_as_live_status(client):
    response = client.post(
        reverse("reviews:register"),
        {
            "username": "new-reviewer",
            "email": "reviewer@example.com",
            "password1": "X9!mQ2#vL7$p",
            "password2": "X9!mQ2#vL7$p",
        },
        follow=True,
    )

    assert response.status_code == 200
    assert b'role="status" aria-live="polite"' in response.content
    assert b"Your account was created." in response.content


def test_movie_detail_uses_semantic_dates_and_accessible_rating(client):
    movie = Movie.objects.create(
        title="Spirited Away",
        release_date=date(2001, 7, 20),
    )
    author = get_user_model().objects.create_user(username="reviewer")
    Review.objects.create(
        movie=movie,
        author=author,
        rating=5,
        body="Beautifully told.",
    )

    response = client.get(reverse("reviews:movie_detail", args=[movie.pk]))

    assert response.status_code == 200
    assert b'<time datetime="2001-07-20">' in response.content
    assert b'aria-label="Rated 5 out of 5"' in response.content
    assert b'<ol class="review-list">' in response.content
