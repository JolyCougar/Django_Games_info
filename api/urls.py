from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from .views import GameViewSet, ReviewCreateViewSet, AddStarRatingViewSet, DeveloperViewSet, PublisherViewSet

urlpatterns = format_suffix_patterns([
    path("game", GameViewSet.as_view({'get': 'list'})),
    path("game/<int:pk>", GameViewSet.as_view({'get': 'retrieve'})),
    path("review", ReviewCreateViewSet.as_view({'post': 'create'})),
    path("rating", AddStarRatingViewSet.as_view({'post': 'create'})),
    path('developer', DeveloperViewSet.as_view({'get': 'list'})),
    path('developer/<int:pk>', DeveloperViewSet.as_view({'get': 'retrieve'})),
    path('publisher', PublisherViewSet.as_view({'get': 'list'})),
    path('publisher/<int:pk>', PublisherViewSet.as_view({'get': 'retrieve'})),

])
