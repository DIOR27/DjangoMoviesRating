from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions
from .models import Movie, Director, Review
from .serializers import MovieSerializer, DirectorSerializer, ReviewSerializer


class DirectorViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class MovieViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ReviewViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# region Reviews


class CriticReviewListView(generics.ListAPIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    queryset = get_queryset
    serializer_class = ReviewSerializer


class CriticReviewUpdateView(generics.UpdateAPIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    queryset = get_queryset
    serializer_class = ReviewSerializer


class CriticReviewDeleteView(generics.DestroyAPIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    queryset = get_queryset
    serializer_class = ReviewSerializer


# endregion Reviews
