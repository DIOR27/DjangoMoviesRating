from datetime import date
from django.db import models
from django.contrib.auth.models import User


class Director(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(date.today)

    def __str__(self):
        return f"{self.name} {self.last_name}"


class Movie(models.Model):
    name = models.CharField(max_length=100)
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True)
    release_date = models.DateField(date.today)
    description = models.TextField(blank=True)
    average_rating = models.FloatField(default=0)


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.rating}/5] - {self.comment}"