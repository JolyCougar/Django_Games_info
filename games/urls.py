from django.urls import path

from .views import GamesView, GameDetailView, PublisherView, DeveloperView

urlpatterns = [
    path("", GamesView.as_view(), name="games_list"),
    path("<slug:slug>/", GameDetailView.as_view(), name="game_detail"),
    path("publisher/<str:slug>/", PublisherView.as_view(), name="publisher_detail"),
    path("developer/<str:slug>/", DeveloperView.as_view(), name="developer_detail"),
]
