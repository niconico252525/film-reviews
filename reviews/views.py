from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from reviews.forms import ReviewForm
from reviews.models import Movie
from reviews.services import (
    get_movie_average_rating,
    get_recent_movies,
    get_user_review,
    save_review,
    search_movies,
)


def home(request):
    """Show the landing page and recently added movies."""
    return render(
        request,
        "reviews/home.html",
        {"recent_movies": get_recent_movies()},
    )


def movie_list(request):
    """Show all movies or title matches for the optional ``q`` argument."""
    query = request.GET.get("q", "").strip()
    return render(
        request,
        "reviews/movie_list.html",
        {"movies": search_movies(query), "query": query},
    )


def movie_detail(request, movie_id):
    """Show one movie, its average rating, and its reviews."""
    movie = get_object_or_404(
        Movie.objects.prefetch_related("reviews__author"),
        pk=movie_id,
    )
    return render(
        request,
        "reviews/movie_detail.html",
        {
            "movie": movie,
            "average_rating": get_movie_average_rating(movie),
            "reviews": movie.reviews.all(),
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def review_create(request, movie_id):
    """Create or update the signed-in user's review, then redirect to detail."""
    movie = get_object_or_404(Movie, pk=movie_id)
    existing_review = get_user_review(movie=movie, author=request.user)
    initial = None
    if existing_review:
        initial = {
            "rating": existing_review.rating,
            "body": existing_review.body,
        }

    form = ReviewForm(
        request.POST if request.method == "POST" else None,
        initial=initial,
    )
    if request.method == "POST" and form.is_valid():
        save_review(
            movie=movie,
            author=request.user,
            rating=form.cleaned_data["rating"],
            body=form.cleaned_data["body"],
        )
        messages.success(request, "Your review was saved.")
        return redirect("reviews:movie_detail", movie_id=movie.pk)

    return render(
        request,
        "reviews/review_form.html",
        {
            "movie": movie,
            "form": form,
            "is_update": existing_review is not None,
        },
    )
