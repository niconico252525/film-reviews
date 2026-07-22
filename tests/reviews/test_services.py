from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

from reviews.models import Movie, Review
from reviews.services import (
    get_movie_average_rating,
    get_recent_movies,
    register_user,
    save_review,
    search_movies,
)

pytestmark = pytest.mark.django_db


def test_unrated_movie_has_no_average():
    movie = Movie.objects.create(title="Unrated")

    assert get_movie_average_rating(movie) is None


def test_average_rating_uses_current_reviews():
    movie = Movie.objects.create(title="Rated")
    first_author = get_user_model().objects.create_user(username="first")
    second_author = get_user_model().objects.create_user(username="second")
    first_review = Review.objects.create(
        movie=movie,
        author=first_author,
        rating=3,
        body="Good.",
    )
    Review.objects.create(
        movie=movie,
        author=second_author,
        rating=5,
        body="Excellent.",
    )

    assert get_movie_average_rating(movie) == 4.0

    first_review.rating = 1
    first_review.save(update_fields=["rating"])
    assert get_movie_average_rating(movie) == 3.0

    first_review.delete()
    assert get_movie_average_rating(movie) == 5.0


def test_recent_movies_returns_newest_movies_up_to_limit():
    older = Movie.objects.create(title="Older")
    newer = Movie.objects.create(title="Newer")
    Movie.objects.filter(pk=older.pk).update(
        created_at=timezone.now() - timedelta(days=1)
    )

    assert list(get_recent_movies(limit=1)) == [newer]


def test_search_movies_returns_all_movies_for_blank_query():
    alien = Movie.objects.create(title="Alien")
    spirited_away = Movie.objects.create(title="Spirited Away")

    assert list(search_movies("  ")) == [alien, spirited_away]


def test_search_movies_matches_partial_title_case_insensitively():
    spirited_away = Movie.objects.create(title="Spirited Away")
    Movie.objects.create(title="Alien")

    assert list(search_movies("  SPIRIT  ")) == [spirited_away]


def test_register_user_persists_email_and_hashed_password():
    user = register_user(
        username="registered-reviewer",
        email="reviewer@example.com",
        password="X9!mQ2#vL7$p",
    )

    assert user.email == "reviewer@example.com"
    assert user.check_password("X9!mQ2#vL7$p")
    assert get_user_model().objects.filter(username="registered-reviewer").exists()


def test_save_review_creates_then_updates_one_review():
    movie = Movie.objects.create(title="Reviewable")
    author = get_user_model().objects.create_user(username="service-reviewer")

    review = save_review(
        movie=movie,
        author=author,
        rating=3,
        body="First version.",
    )
    updated_review = save_review(
        movie=movie,
        author=author,
        rating=5,
        body="Updated version.",
    )

    assert updated_review.pk == review.pk
    assert Review.objects.count() == 1
    updated_review.refresh_from_db()
    assert updated_review.rating == 5
    assert updated_review.body == "Updated version."


def test_save_review_validates_before_writing():
    movie = Movie.objects.create(title="Reviewable")
    author = get_user_model().objects.create_user(username="invalid-reviewer")

    with pytest.raises(ValidationError):
        save_review(
            movie=movie,
            author=author,
            rating=6,
            body="Invalid rating.",
        )

    assert Review.objects.count() == 0
