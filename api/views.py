from django.db import models
from rest_framework import generics, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .service import get_client_ip, GamesFilter, PaginationGames
from games.models import Game, Developer, Publisher, Genres
from .serializers import (GamesListSerializer, GameDetailSerializer,
                          ReviewCreateSerializer, CreateRatingSerializer,
                          PublisherListSerializer, PublisherDetailSerializer,
                          DeveloperListSerializer, DeveloperDetailSerializer,
                          GenreListSerializer, GenreDetailSerializer)


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filter_class = GamesFilter
    pagination_class = PaginationGames

    def get_queryset(self):
        movies = Game.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings",
                                     filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return GamesListSerializer
        elif self.action == 'retrieve':
            return GameDetailSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewCreateSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class PublisherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Publisher.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return PublisherListSerializer
        elif self.action == 'retrieve':
            return PublisherDetailSerializer


class GenresViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genres.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return GenreListSerializer
        elif self.action == 'retrieve':
            return GenreDetailSerializer


class DeveloperViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Developer.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return DeveloperListSerializer
        elif self.action == 'retrieve':
            return DeveloperDetailSerializer
