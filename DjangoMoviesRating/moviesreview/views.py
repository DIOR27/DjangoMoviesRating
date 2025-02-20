from rest_framework import generics, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
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

    def _check_group(self, request, review):
        """
        Verifica si el usuario autenticado tiene permiso para acceder a la
        rese a proporcionada.

        Si el usuario es el dueño de la reseña o pertenece al grupo
        "Movies Administrators", el método devuelve True. De lo contrario,
        devuelve una respuesta de error 403.

        :param request: La solicitud HTTP que contiene la informaci n del usuario
        autenticado.
        :param review: La rese a a la que se intenta acceder.
        :return: True si el usuario tiene permiso, o una respuesta de error 403 en
        caso contrario.
        """

        if request.user.groups.filter(name="Movies Administrators").exists():
            return True

        return Response(
            {"detail": "Solo los administradores pueden acceder a este endpoint."},
            status=status.HTTP_403_FORBIDDEN,
        )

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

        review = self.get_object()
        permission_check = self._check_group(request, review)

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
        review = self.get_object()
        permission_check = self._check_group(request, review)

        if isinstance(permission_check, Response):
            return permission_check  # Retorna la respuesta 403 si no tiene permisos

        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        review = self.get_object()
        permission_check = self._check_group(request, review)

        if isinstance(permission_check, Response):
            return permission_check  # Retorna 403 si no tiene permisos

        return super().destroy(request, *args, **kwargs)


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
