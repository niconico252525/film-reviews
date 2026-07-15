from datetime import date

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from reviews.models import Movie, Review

pytestmark = pytest.mark.django_db


@pytest.fixture
def author():
    return get_user_model().objects.create_user(
        username="reviewer",
        password="test-password",
    )


@pytest.fixture
def movie():
    return Movie.objects.create(
        title="Spirited Away",
        release_date=date(2001, 7, 20),
    )


def test_movie_string_includes_release_year():
    movie = Movie(title="Spirited Away", release_date=date(2001, 7, 20))

    assert str(movie) == "Spirited Away (2001)"


def test_movie_string_without_release_date_uses_title():
    movie = Movie(title="Untitled Film")

    assert str(movie) == "Untitled Film"


def test_movies_may_share_a_title():
    Movie.objects.create(title="The Thing", release_date=date(1951, 4, 6))
    Movie.objects.create(title="The Thing", release_date=date(1982, 6, 25))

    assert Movie.objects.filter(title="The Thing").count() == 2


def test_review_string_identifies_author_movie_and_rating(author, movie):
    review = Review.objects.create(
        author=author,
        movie=movie,
        rating=5,
        body="A beautiful film.",
    )

    assert str(review) == "reviewer — Spirited Away (2001) (5/5)"


def test_review_is_available_from_author_and_movie(author, movie):
    review = Review.objects.create(
        author=author,
        movie=movie,
        rating=5,
        body="A beautiful film.",
    )

    assert movie.reviews.get() == review
    assert author.reviews.get() == review


@pytest.mark.parametrize("rating", [1, 5])
def test_rating_validation_accepts_boundaries(author, movie, rating):
    review = Review(
        author=author,
        movie=movie,
        rating=rating,
        body="Boundary rating.",
    )

    review.full_clean()


@pytest.mark.parametrize("rating", [0, 6])
def test_rating_validation_rejects_out_of_range_values(author, movie, rating):
    review = Review(
        author=author,
        movie=movie,
        rating=rating,
        body="Invalid rating.",
    )

    with pytest.raises(ValidationError, match="rating"):
        review.full_clean()


@pytest.mark.parametrize("rating", [0, 6])
def test_database_rejects_out_of_range_ratings(author, movie, rating):
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            Review.objects.create(
                author=author,
                movie=movie,
                rating=rating,
                body="Invalid rating.",
            )


def test_database_rejects_a_second_review_by_same_author(author, movie):
    Review.objects.create(
        author=author,
        movie=movie,
        rating=4,
        body="First review.",
    )

    with pytest.raises(IntegrityError):
        with transaction.atomic():
            Review.objects.create(
                author=author,
                movie=movie,
                rating=5,
                body="Duplicate review.",
            )


def test_different_authors_may_review_the_same_movie(author, movie):
    another_author = get_user_model().objects.create_user(username="another")
    Review.objects.create(author=author, movie=movie, rating=4, body="Good.")
    Review.objects.create(
        author=another_author,
        movie=movie,
        rating=5,
        body="Excellent.",
    )

    assert movie.reviews.count() == 2


def test_deleting_movie_cascades_to_reviews(author, movie):
    Review.objects.create(author=author, movie=movie, rating=4, body="Good.")

    movie.delete()

    assert Review.objects.count() == 0


def test_deleting_author_cascades_to_reviews(author, movie):
    Review.objects.create(author=author, movie=movie, rating=4, body="Good.")

    author.delete()

    assert Review.objects.count() == 0
