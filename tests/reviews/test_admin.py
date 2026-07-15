import pytest
from django.contrib import admin
from django.contrib.auth import get_user_model

from reviews.models import Movie, Review


def test_movie_is_registered_with_admin():
    assert admin.site.is_registered(Movie)


def test_review_is_registered_with_admin():
    assert admin.site.is_registered(Review)


@pytest.mark.django_db
def test_movie_admin_displays_formatted_average_rating():
    movie = Movie.objects.create(title="Admin Film")
    movie_admin = admin.site._registry[Movie]

    assert movie_admin.average_rating(movie) == "—"

    author = get_user_model().objects.create_user(username="admin-reviewer")
    Review.objects.create(
        movie=movie,
        author=author,
        rating=4,
        body="A review for the admin list.",
    )

    assert movie_admin.average_rating(movie) == "4.0"
