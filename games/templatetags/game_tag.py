from django import template
from games.models import Genres, Game

register = template.Library()


@register.simple_tag()
def get_genres():
    """ View all genres """
    return Genres.objects.all()


@register.inclusion_tag('games/tags/last_games.html')
def get_last_games(count):
    games = Game.objects.order_by("id")[:count]
    return {"last_game": games}
