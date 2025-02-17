from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DirectorViewSet,
    ReviewViewSet,
    MovieViewSet,
    CriticReviewListView,
)

defaultRouter = DefaultRouter()
defaultRouter.register("directors", DirectorViewSet)
defaultRouter.register("reviews", ReviewViewSet)
defaultRouter.register("movies", MovieViewSet)

urlpatterns = [
    path('reviews/critic/', CriticReviewListView.as_view(), name="reviews-list"),
]

urlpatterns += defaultRouter.urls