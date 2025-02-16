from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions
from .models import Movie, Director, Review
from .serializers import MovieSerializer, DirectorSerializer, ReviewSerializer

class DirectorViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class ReviewListView(generics.ListAPIView):
    permission_classes = [DjangoModelPermissions]
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
    
    queryset = get_queryset
    serializer_class = ReviewSerializer

class ReviewCreateView(generics.CreateAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer