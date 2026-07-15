from django.contrib import admin

from reviews.models import Movie, Review
from reviews.services import get_movie_average_rating


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_date", "average_rating", "created_at")
    search_fields = ("title",)
    ordering = ("title",)

    @admin.display(description="Average rating")
    def average_rating(self, movie):
        average = get_movie_average_rating(movie)
        return "—" if average is None else f"{average:.1f}"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("movie", "author", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("movie__title", "author__username", "body")
    autocomplete_fields = ("movie", "author")
    ordering = ("-created_at",)
