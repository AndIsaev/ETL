from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from rest_framework import mixins, viewsets
from .serializers import MoviesSerializer
from movies.models import FilmWork


class MoviesAPIView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):

    serializer_class = MoviesSerializer

    def get_queryset(self):
        queryset = FilmWork.objects.values(
            "id", "title", "description", "creation_date", "rating", "type"
        ).annotate(
            actors=ArrayAgg(
                "persons__full_name",
                filter=Q(person_film_work__role="actor"),
                distinct=True,
            ),
            directors=ArrayAgg(
                "persons__full_name",
                filter=Q(person_film_work__role="director"),
                distinct=True,
            ),
            writers=ArrayAgg(
                "persons__full_name",
                filter=Q(person_film_work__role="writer"),
                distinct=True,
            ),
            genres=ArrayAgg("genres__name", distinct=True),
        )
        return queryset
