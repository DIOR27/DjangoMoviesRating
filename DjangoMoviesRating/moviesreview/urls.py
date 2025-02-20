from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DirectorViewSet,
    ReviewViewSet,
    MovieViewSet,
    CriticReviewListView,
    CriticReviewUpdateView,
    CriticReviewDeleteView,
)

defaultRouter = DefaultRouter()
defaultRouter.register("directors", DirectorViewSet)
defaultRouter.register("reviews", ReviewViewSet)
defaultRouter.register("movies", MovieViewSet)

urlpatterns = [
    path('reviews/critic/', CriticReviewListView.as_view(), name="reviews-list"),
    path('reviews/critic/<int:pk>/', CriticReviewUpdateView.as_view(), name="reviews-update"),
    path('reviews/critic/<int:pk>/', CriticReviewDeleteView.as_view(), name="reviews-delete"),
]

urlpatterns += defaultRouter.urls