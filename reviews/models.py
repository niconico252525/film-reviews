from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    release_date = models.DateField(blank=True, null=True)
    synopsis = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title", "release_date", "pk"]

    def __str__(self):
        if self.release_date:
            return f"{self.title} ({self.release_date.year})"
        return self.title


class Review(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "-pk"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(rating__gte=1, rating__lte=5),
                name="reviews_rating_between_1_and_5",
            ),
            models.UniqueConstraint(
                fields=["author", "movie"],
                name="reviews_unique_author_movie",
            ),
        ]

    def __str__(self):
        return f"{self.author} — {self.movie} ({self.rating}/5)"
