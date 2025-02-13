from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from .models import Movie, Director, Review
from .serializers import MovieSerializer, DirectorSerializer, ReviewSerializer

class DirectorViewSet(ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class ReviewListView(generics.ListAPIView):
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
    
    queryset = get_queryset
    serializer_class = ReviewSerializer