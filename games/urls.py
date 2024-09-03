from django.urls import path

from .views import GamesView, GameDetailView, PublisherView, DeveloperView, AddStarRating, AddReview

urlpatterns = [
    path("", GamesView.as_view(), name="games_list"),
    path("add-rating/", AddStarRating.as_view(), name='add_rating'),
    path("<slug:slug>/", GameDetailView.as_view(), name="game_detail"),
    path("publisher/<str:slug>/", PublisherView.as_view(), name="publisher_detail"),
    path("developer/<str:slug>/", DeveloperView.as_view(), name="developer_detail"),
    path("review/<int:pk>/", AddReview.as_view(), name="add_review"),
]
