import pytest

from reviews.forms import MovieSearchForm, RegistrationForm, ReviewForm


def test_movie_search_form_strips_valid_query():
    form = MovieSearchForm({"q": "  SPIRIT  "})

    assert form.is_valid()
    assert form.cleaned_data["q"] == "SPIRIT"


def test_movie_search_form_accepts_blank_query():
    form = MovieSearchForm({"q": "   "})

    assert form.is_valid()
    assert form.cleaned_data["q"] == ""


def test_movie_search_form_rejects_query_over_255_characters():
    form = MovieSearchForm({"q": "x" * 256})

    assert not form.is_valid()
    assert "q" in form.errors


@pytest.mark.django_db
def test_registration_form_accepts_valid_user_input():
    form = RegistrationForm(
        {
            "username": "new-reviewer",
            "email": "reviewer@example.com",
            "password1": "X9!mQ2#vL7$p",
            "password2": "X9!mQ2#vL7$p",
        }
    )

    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_registration_form_rejects_invalid_email_and_password_confirmation():
    form = RegistrationForm(
        {
            "username": "new-reviewer",
            "email": "not-an-email",
            "password1": "X9!mQ2#vL7$p",
            "password2": "different-password",
        }
    )

    assert not form.is_valid()
    assert set(form.errors) == {"email", "password2"}


def test_review_form_rejects_invalid_rating_and_whitespace_only_body():
    form = ReviewForm({"rating": "6", "body": "   "})

    assert not form.is_valid()
    assert set(form.errors) == {"rating", "body"}
