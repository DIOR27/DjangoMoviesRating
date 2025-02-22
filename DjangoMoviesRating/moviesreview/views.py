from django.db.models import Avg
from rest_framework import generics, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Movie, Director, Review
from .serializers import MovieSerializer, DirectorSerializer, ReviewSerializer


class ReviewViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        review = serializer.save(user=self.request.user)
        self.update_movie_rating(review.movie)

    def _check_group(self, request):
        """
        Verifica si el usuario autenticado tiene permiso para acceder a la
        reseña proporcionada.

        Si el usuario es el dueño de la reseña o pertenece al grupo
        "Movies Administrators", el método devuelve True. De lo contrario,
        devuelve una respuesta de error 403.

        :param request: La solicitud HTTP que contiene la información del usuario
        autenticado.
        :param review: La reseña a la que se intenta acceder.
        :return: True si el usuario tiene permiso, o una respuesta de error 403 en
        caso contrario.
        """

        if request.user.groups.filter(name="Movies Administrators").exists():
            return True

        return Response(
            {"detail": "Solo los administradores pueden acceder a este endpoint."},
            status=status.HTTP_403_FORBIDDEN,
        )

    def perform_update(self, serializer):
        """
        Actualiza la reseña y recalcula el promedio de calificación de la película.
        """
        review = self.get_object()
        serializer.save()
        self.update_movie_rating(review.movie)

    def update(self, request, *args, **kwargs):
        """
        Actualiza una reseña existente.

        Este método verifica si el usuario autenticado tiene permiso para editar
        la reseña. Si el usuario es el dueño de la reseña o pertenece al grupo
        "Movies Administrators", el proceso de actualización continúa. De lo
        contrario, se devuelve una respuesta de error 403.

        :param request: La solicitud HTTP que contiene los datos de actualización.
        :param args: Argumentos adicionales.
        :param kwargs: Argumentos adicionales con nombre.
        :return: Una respuesta HTTP con el resultado de la operación de actualización.
        """

        permission_check = self._check_group(request)

        if isinstance(permission_check, Response):
            return permission_check  # Retorna la respuesta 403 si no tiene permisos

        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Actualiza parcialmente una reseña existente.

        Este método verifica si el usuario autenticado tiene permiso para editar
        la reseña. Si el usuario es el due o de la reseña o pertenece al grupo
        "Movies Administrators", el proceso de actualización parcial continua.
        De lo contrario, se devuelve una respuesta de error 403.

        :param request: La solicitud HTTP que contiene los datos de actualización.
        :param args: Argumentos adicionales.
        :param kwargs: Argumentos adicionales con nombre.
        :return: Una respuesta HTTP con el resultado de la operación de actualización.
        """
        permission_check = self._check_group(request)

        if isinstance(permission_check, Response):
            return permission_check  # Retorna la respuesta 403 si no tiene permisos

        return super().partial_update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        """
        Elimina la reseña y recalcula el promedio de calificación de la película.
        """
        movie = instance.movie
        instance.delete()
        self.update_movie_rating(movie)

    def destroy(self, request, *args, **kwargs):
        permission_check = self._check_group(request)

        if isinstance(permission_check, Response):
            return permission_check  # Retorna 403 si no tiene permisos

        return super().destroy(request, *args, **kwargs)

    def update_movie_rating(self, movie):
        """
        Calcula y actualiza el `average_rating` de una película basada en sus reseñas.
        """
        avg_rating = (
            Review.objects.filter(movie=movie).aggregate(Avg("rating"))["rating__avg"]
            or 0
        )
        movie.average_rating = round(avg_rating, 2)  # Redondear a 2 decimales
        movie.save()


# region Reviews


class CriticReviewListView(generics.ListAPIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    queryset = get_queryset
    serializer_class = ReviewSerializer


class CriticReviewMovieListView(generics.ListAPIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        movie_id = self.kwargs.get("movie_id")
        return Review.objects.filter(
            user=self.request.user, movie_id=movie_id
        ).order_by("-updated_at")

    queryset = get_queryset
    serializer_class = ReviewSerializer


class CriticReviewUpdateView(generics.UpdateAPIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    queryset = get_queryset
    serializer_class = ReviewSerializer

    def perform_update(self, serializer):
        """
        Actualiza la reseña y recalcula el promedio de calificación de la película.
        """
        review = self.get_object()
        serializer.save()
        self.update_movie_rating(review.movie)

    def update_movie_rating(self, movie):
        """
        Calcula y actualiza el `average_rating` de una película basada en sus reseñas.
        """
        avg_rating = (
            Review.objects.filter(movie=movie).aggregate(Avg("rating"))["rating__avg"]
            or 0
        )
        movie.average_rating = round(avg_rating, 2)  # Redondear a 2 decimales
        movie.save()


class CriticReviewDeleteView(generics.DestroyAPIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    queryset = get_queryset
    serializer_class = ReviewSerializer


# endregion Reviews


# region Movies
class MovieListView(generics.ListAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieCreateView(generics.CreateAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieUpdateView(generics.UpdateAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieDeleteView(generics.DestroyAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


# endregion Movies


# region Directors
class DirectorListView(generics.ListAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class DirectorCreateView(generics.CreateAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class DirectorUpdateView(generics.UpdateAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class DirectorDeleteView(generics.DestroyAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


@api_view(["GET"])
def top_movies(request, top_number):
    """
    Devuelve las n películas mejor calificadas.
    """
    top_movies = Movie.objects.order_by("-average_rating")[:top_number]
    if not top_movies:
        return Response(
            {"detail": "No hay películas disponibles en este momento."},
            status=status.HTTP_404_NOT_FOUND,
        )
    serializer = MovieSerializer(top_movies, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])  # Solo usuarios autenticados pueden acceder
def top_movies_by_user(request, top_number):
    """
    Devuelve las N películas mejor calificadas por el usuario autenticado.
    """
    user = request.user  # Obtener el usuario autenticado

    # Filtrar las reseñas del usuario y calcular el promedio de calificación por película
    movies_rated_by_user = (
        Review.objects.filter(user=user)
        .values("movie")
        .annotate(user_avg_rating=Avg("rating"))
        .order_by("-user_avg_rating")[:top_number]
    )

    if not movies_rated_by_user:
        return Response(
            {"detail": "No has calificado ninguna película."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Obtener las películas correspondientes
    movie_ids = [entry["movie"] for entry in movies_rated_by_user]
    movies = Movie.objects.filter(id__in=movie_ids)

    # Serializar y devolver los datos
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)
