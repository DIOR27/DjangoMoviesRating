from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ReviewViewSet,
    CriticReviewListView,
    CriticReviewUpdateView,
    CriticReviewDeleteView,
)

defaultRouter = DefaultRouter()
defaultRouter.register("reviews", ReviewViewSet)

urlpatterns = [
    path('reviews/critic/', CriticReviewListView.as_view(), name="reviews-list"),
    path('reviews/critic/<int:pk>/', CriticReviewUpdateView.as_view(), name="reviews-update"),
    path('reviews/critic/<int:pk>/', CriticReviewDeleteView.as_view(), name="reviews-delete"),
]

urlpatterns += defaultRouter.urls