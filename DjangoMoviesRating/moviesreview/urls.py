from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DirectorViewSet,
    ReviewListView,
    ReviewCreateView,
)

director_router = DefaultRouter()
director_router.register("directors", DirectorViewSet)

urlpatterns = [
    path('reviews/', ReviewListView.as_view(), name="reviews-list"),
    path('reviews/', ReviewCreateView.as_view(), name="reviews-create"),
]

urlpatterns += director_router.urls