from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Game, Publisher, Developer


class GamesView(ListView):
    model = Game
    queryset = Game.objects.filter(draft=False).all()
    template_name = "games/games_list.html"


class GameDetailView(DetailView):
    model = Game
    queryset = Game.objects.filter(draft=False)
    slug_field = "url"


class PublisherView(DetailView):
    model = Publisher
    template_name = "games/publisher_view.html"
    slug_field = "name"


class DeveloperView(DetailView):
    model = Developer
    template_name = "games/developer_view.html"
    slug_field = "name"
