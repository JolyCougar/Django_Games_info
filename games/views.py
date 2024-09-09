from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.views.generic.base import View
from django.shortcuts import redirect
from django.http import HttpResponse
from .forms import RatingForm, ReviewForm
from django.db.models import Avg

from .models import Game, Publisher, Developer, Rating, Genres, GamePlatform


class GenreYear:
    """ Genres and year of games """

    def get_platform(self):
        return GamePlatform.objects.all()


class GamesView(GenreYear, ListView):
    model = Game
    queryset = Game.objects.filter(draft=False).all()
    template_name = "games/game_list.html"


class GameDetailView(GenreYear, DetailView):
    model = Game
    queryset = Game.objects.filter(draft=False)
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        context['star'] = Game.objects.aggregate(avg=Avg('ratings__star'))
        context["form"] = ReviewForm()
        return context


class PublisherView(GenreYear, DetailView):
    model = Publisher
    template_name = "games/publisher_view.html"
    slug_field = "name"


class DeveloperView(GenreYear, DetailView):
    model = Developer
    template_name = "games/developer_view.html"
    slug_field = "name"


class AddStarRating(View):

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                game_id=int(request.POST.get("game")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class AddReview(View):
    """ Review for game """

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        game = Game.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.game = game
            form.save()
        return redirect(game.get_absolute_url())


class FilterGamesView(GenreYear, ListView):
    """ Filter games """
    paginate_by = 2

    def get_queryset(self):
        queryset = Game.objects.filter(Q(game_platform__in=self.request.GET.getlist("game_platform")) |
                                       Q(genres__in=self.request.GET.getlist("genre"))
                                       ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["game_platform"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("game_platform")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context


class Search(GenreYear, ListView):
    """ Search games """
    paginate_by = 2

    def get_queryset(self):
        q = self.request.GET.get('q')
        a = "".join(q[0].upper()) + q[1:]
        return Game.objects.filter(name__icontains=a)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context
