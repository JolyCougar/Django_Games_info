from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Game


class GamesView(ListView):
    model = Game
    queryset = Game.objects.filter(draft=False).all()
    template_name = "games/games_list.html"

