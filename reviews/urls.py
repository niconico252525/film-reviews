from django.urls import path

from reviews import views

app_name = "reviews"

urlpatterns = [
    path("", views.home, name="home"),
    path("movies/", views.movie_list, name="movie_list"),
    path("movies/<int:movie_id>/", views.movie_detail, name="movie_detail"),
    path(
        "movies/<int:movie_id>/reviews/new/",
        views.review_create,
        name="review_create",
    ),
]
