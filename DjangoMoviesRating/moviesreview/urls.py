from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ReviewViewSet,
    CriticReviewListView,
    CriticReviewMovieListView,
    CriticReviewUpdateView,
    CriticReviewDeleteView,
    MovieListView,
    MovieCreateView,
    MovieUpdateView,
    MovieDeleteView,
    DirectorListView,
    DirectorCreateView,
    DirectorUpdateView,
    DirectorDeleteView,
    top_movies,
)

defaultRouter = DefaultRouter()
defaultRouter.register("reviews", ReviewViewSet)

urlpatterns = [
    path("reviews/critic/", CriticReviewListView.as_view(), name="reviews-list"),
    path(
        "reviews/critic/<int:movie_id>/",
        CriticReviewMovieListView.as_view(),
        name="reviews-list",
    ),
    path(
        "reviews/critic/update/<int:pk>/",
        CriticReviewUpdateView.as_view(),
        name="reviews-update",
    ),
    path(
        "reviews/critic/delete/<int:pk>/",
        CriticReviewDeleteView.as_view(),
        name="reviews-delete",
    ),
    path("movies/", MovieListView.as_view(), name="movies-list"),
    path("movies/create/", MovieCreateView.as_view(), name="movies-create"),
    path("movies/update/<int:pk>/", MovieUpdateView.as_view(), name="movies-update"),
    path("movies/delete/<int:pk>/", MovieDeleteView.as_view(), name="movies-delete"),
    path("directors/", DirectorListView.as_view(), name="directors-list"),
    path("directors/create/", DirectorCreateView.as_view(), name="directors-create"),
    path(
        "directors/update/<int:pk>/",
        DirectorUpdateView.as_view(),
        name="directors-update",
    ),
    path(
        "directors/delete/<int:pk>/",
        DirectorDeleteView.as_view(),
        name="directors-delete",
    ),
    path("movies/top/<int:top_number>/", top_movies, name="top-movies"),
]

urlpatterns += defaultRouter.urls
