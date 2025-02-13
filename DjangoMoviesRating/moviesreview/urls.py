from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DirectorViewSet,
    ReviewListView,
)

director_router = DefaultRouter()
director_router.register("directors", DirectorViewSet)

urlpatterns = [
    path('reviews/', ReviewListView.as_view(), name="reviews-list"),
]

urlpatterns += director_router.urls