from typing import Optional

from django.db.models import Avg

from reviews.models import Movie, Review


def get_recent_movies(limit: int = 5):
    """Return the most recently added movies, newest first."""
    return Movie.objects.order_by("-created_at", "-pk")[:limit]


def search_movies(query: str = ""):
    """Return all movies, optionally filtered by a partial title."""
    movies = Movie.objects.all()
    query = query.strip()
    if query:
        movies = movies.filter(title__icontains=query)
    return movies


def get_movie_average_rating(movie: Movie) -> Optional[float]:
    """Return the current average rating, or ``None`` for an unrated movie."""
    average = movie.reviews.aggregate(average=Avg("rating"))["average"]
    return float(average) if average is not None else None


def get_user_review(*, movie: Movie, author):
    """Return an author's review for a movie, if one exists."""
    return Review.objects.filter(movie=movie, author=author).first()


def save_review(*, movie: Movie, author, rating: int, body: str) -> Review:
    """Create or update the author's single review for a movie."""
    review = get_user_review(movie=movie, author=author)
    if review is None:
        review = Review(movie=movie, author=author)

    review.rating = rating
    review.body = body
    review.full_clean()
    review.save()
    return review
