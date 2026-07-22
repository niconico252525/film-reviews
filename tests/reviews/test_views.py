from datetime import date

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from reviews.models import Movie, Review

pytestmark = pytest.mark.django_db


@pytest.fixture
def movie():
    return Movie.objects.create(
        title="Spirited Away",
        release_date=date(2001, 7, 20),
        synopsis="A girl enters a mysterious spirit world.",
    )


@pytest.fixture
def user():
    return get_user_model().objects.create_user(
        username="view-reviewer",
        password="test-password",
    )


def test_home_renders_recent_movies(client, movie):
    response = client.get(reverse("reviews:home"))

    assert response.status_code == 200
    assert response.context["recent_movies"][0] == movie
    assert "reviews/home.html" in [template.name for template in response.templates]
    assert movie.title.encode() in response.content


def test_movie_list_renders_all_movies(client, movie):
    another_movie = Movie.objects.create(title="Alien")

    response = client.get(reverse("reviews:movie_list"))

    assert response.status_code == 200
    assert list(response.context["movies"]) == [another_movie, movie]
    assert response.context["query"] == ""
    assert not response.context["search_form"].is_bound


def test_movie_list_filters_by_trimmed_case_insensitive_query(client, movie):
    Movie.objects.create(title="Alien")

    response = client.get(reverse("reviews:movie_list"), {"q": " SPIRIT "})

    assert response.status_code == 200
    assert list(response.context["movies"]) == [movie]
    assert response.context["query"] == "SPIRIT"
    assert b"Alien" not in response.content


def test_movie_list_rejects_oversized_query_without_returning_movies(client, movie):
    response = client.get(reverse("reviews:movie_list"), {"q": "x" * 256})

    assert response.status_code == 200
    assert response.context["movies"] == ()
    assert "q" in response.context["search_form"].errors
    assert movie.title.encode() not in response.content


def test_movie_list_rejects_post_requests(client):
    response = client.post(reverse("reviews:movie_list"), {"q": "Alien"})

    assert response.status_code == 405


def test_movie_detail_renders_rating_and_reviews(client, movie, user):
    review = Review.objects.create(
        movie=movie,
        author=user,
        rating=4,
        body="A memorable adventure.",
    )

    response = client.get(reverse("reviews:movie_detail", args=[movie.pk]))

    assert response.status_code == 200
    assert response.context["movie"] == movie
    assert response.context["average_rating"] == 4.0
    assert list(response.context["reviews"]) == [review]
    assert b"4.0/5" in response.content
    assert review.body.encode() in response.content


def test_movie_detail_returns_404_for_unknown_movie(client):
    response = client.get(reverse("reviews:movie_detail", args=[999999]))

    assert response.status_code == 404


def test_anonymous_user_is_redirected_to_login_for_review_form(client, movie):
    review_url = reverse("reviews:review_create", args=[movie.pk])

    response = client.get(review_url)

    assert response.status_code == 302
    assert response.url == f"{reverse('login')}?next={review_url}"


def test_review_form_returns_404_for_unknown_movie_after_login(client, user):
    client.force_login(user)

    response = client.get(reverse("reviews:review_create", args=[999999]))

    assert response.status_code == 404


def test_review_form_renders_existing_values_for_authenticated_user(
    client, movie, user
):
    Review.objects.create(
        movie=movie,
        author=user,
        rating=3,
        body="Existing review.",
    )
    client.force_login(user)

    response = client.get(reverse("reviews:review_create", args=[movie.pk]))

    assert response.status_code == 200
    assert response.context["is_update"] is True
    assert response.context["form"].initial == {
        "rating": 3,
        "body": "Existing review.",
    }
    assert b"Update your review" in response.content


def test_valid_review_post_creates_review_and_redirects(client, movie, user):
    client.force_login(user)

    response = client.post(
        reverse("reviews:review_create", args=[movie.pk]),
        {"rating": "5", "body": "Excellent."},
    )

    assert response.status_code == 302
    assert response.url == reverse("reviews:movie_detail", args=[movie.pk])
    review = Review.objects.get(movie=movie, author=user)
    assert review.rating == 5
    assert review.body == "Excellent."


def test_second_review_post_updates_existing_review(client, movie, user):
    review = Review.objects.create(
        movie=movie,
        author=user,
        rating=2,
        body="Original.",
    )
    client.force_login(user)

    response = client.post(
        reverse("reviews:review_create", args=[movie.pk]),
        {"rating": "4", "body": "Reconsidered."},
    )

    assert response.status_code == 302
    assert Review.objects.filter(movie=movie, author=user).count() == 1
    review.refresh_from_db()
    assert review.rating == 4
    assert review.body == "Reconsidered."


def test_invalid_review_post_redisplays_errors_without_writing(client, movie, user):
    client.force_login(user)

    response = client.post(
        reverse("reviews:review_create", args=[movie.pk]),
        {"rating": "6", "body": "   "},
    )

    assert response.status_code == 200
    assert set(response.context["form"].errors) == {"rating", "body"}
    assert Review.objects.count() == 0


def test_review_view_rejects_unsupported_http_method(client, movie, user):
    client.force_login(user)

    response = client.put(reverse("reviews:review_create", args=[movie.pk]))

    assert response.status_code == 405


def test_login_page_is_runnable(client):
    response = client.get(reverse("login"))

    assert response.status_code == 200
    assert "registration/login.html" in [
        template.name for template in response.templates
    ]


def test_registration_page_renders_form_and_shared_navigation(client):
    response = client.get(reverse("reviews:register"))

    assert response.status_code == 200
    assert "registration/register.html" in [
        template.name for template in response.templates
    ]
    assert b"Create account" in response.content
    assert b'name="email"' in response.content


def test_valid_registration_creates_and_signs_in_user(client):
    response = client.post(
        reverse("reviews:register"),
        {
            "username": "new-reviewer",
            "email": "reviewer@example.com",
            "password1": "X9!mQ2#vL7$p",
            "password2": "X9!mQ2#vL7$p",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("reviews:home")
    registered_user = get_user_model().objects.get(username="new-reviewer")
    assert registered_user.email == "reviewer@example.com"
    assert client.session["_auth_user_id"] == str(registered_user.pk)


def test_invalid_registration_redisplays_errors_without_creating_user(client, user):
    response = client.post(
        reverse("reviews:register"),
        {
            "username": user.username,
            "email": "not-an-email",
            "password1": "X9!mQ2#vL7$p",
            "password2": "different-password",
        },
    )

    assert response.status_code == 200
    assert set(response.context["form"].errors) == {
        "username",
        "email",
        "password2",
    }
    assert get_user_model().objects.count() == 1
    assert b"not-an-email" in response.content
    assert b"X9!mQ2#vL7$p" not in response.content


def test_authenticated_user_is_redirected_away_from_registration(client, user):
    client.force_login(user)

    response = client.get(reverse("reviews:register"))

    assert response.status_code == 302
    assert response.url == reverse("reviews:home")


def test_registration_rejects_unsupported_http_method(client):
    response = client.put(reverse("reviews:register"))

    assert response.status_code == 405


def test_logout_redirects_home(client, user):
    client.force_login(user)

    response = client.post(reverse("logout"))

    assert response.status_code == 302
    assert response.url == reverse("reviews:home")
