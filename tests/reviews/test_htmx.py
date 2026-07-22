import pytest
from django.urls import reverse

from reviews.models import Movie

pytestmark = pytest.mark.django_db


def test_movie_page_loads_pinned_htmx_and_defines_live_search(client):
    response = client.get(reverse("reviews:movie_list"))
    content = response.content.decode()

    assert response.status_code == 200
    assert "https://cdn.jsdelivr.net/npm/htmx.org@2.0.10/dist/htmx.min.js" in content
    assert (
        'integrity="sha384-H5SrcfygHmAuTDZphMHqBJLc3FhssKjG7w/CeCpFReSfwBWDTKpkzPP8c+cLsK+V"'
        in content
    )
    assert 'hx-get="/movies/"' in content
    assert (
        'hx-trigger="input changed delay:350ms from:#id_q, search from:#id_q, submit"'
        in content
    )
    assert 'hx-target="#movie-results"' in content
    assert 'hx-push-url="true"' in content
    assert 'hx-sync="this:replace"' in content
    assert 'action="/movies/"' in content
    assert 'method="get"' in content


def test_normal_search_returns_complete_page_and_varies_on_htmx_header(client):
    Movie.objects.create(title="Alien")

    response = client.get(reverse("reviews:movie_list"), {"q": "alien"})

    assert response.status_code == 200
    assert "reviews/movie_list.html" in [
        template.name for template in response.templates
    ]
    assert b"<!doctype html>" in response.content
    assert b'id="movie-results"' in response.content
    assert "HX-Request" in response.headers["Vary"]


def test_htmx_search_returns_only_filtered_results_partial(client):
    alien = Movie.objects.create(title="Alien")
    Movie.objects.create(title="Spirited Away")

    response = client.get(
        reverse("reviews:movie_list"),
        {"q": "alien"},
        HTTP_HX_REQUEST="true",
    )

    template_names = [template.name for template in response.templates]
    assert response.status_code == 200
    assert template_names == ["reviews/partials/movie_results.html"]
    assert response.context["is_htmx"] is True
    assert list(response.context["movies"]) == [alien]
    assert b"<!doctype html>" not in response.content
    assert b'id="movie-results"' not in response.content
    assert b"Alien" in response.content
    assert b"Spirited Away" not in response.content
    assert b"1 movie matching" in response.content
    assert "HX-Request" in response.headers["Vary"]


def test_htmx_blank_search_returns_all_movies(client):
    alien = Movie.objects.create(title="Alien")
    spirited_away = Movie.objects.create(title="Spirited Away")

    response = client.get(
        reverse("reviews:movie_list"),
        {"q": ""},
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert list(response.context["movies"]) == [alien, spirited_away]
    assert b"2 movies" in response.content


def test_invalid_htmx_search_returns_accessible_error_partial(client):
    Movie.objects.create(title="Alien")

    response = client.get(
        reverse("reviews:movie_list"),
        {"q": "x" * 256},
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert response.context["movies"] == ()
    assert b'class="form-error-summary" role="alert"' in response.content
    assert b'href="#id_q"' in response.content
    assert b"Correct the search field to see results." in response.content
    assert b"Alien" not in response.content
