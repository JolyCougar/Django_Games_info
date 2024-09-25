from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (GameViewSet, ReviewCreateViewSet,
                    AddStarRatingViewSet, DeveloperViewSet,
                    PublisherViewSet, GenresViewSet)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = format_suffix_patterns([
    path("game", GameViewSet.as_view({'get': 'list'})),
    path("game/<int:pk>", GameViewSet.as_view({'get': 'retrieve'})),
    path("review", ReviewCreateViewSet.as_view({'post': 'create'})),
    path("rating", AddStarRatingViewSet.as_view({'post': 'create'})),
    path('developer', DeveloperViewSet.as_view({'get': 'list'})),
    path('developer/<int:pk>', DeveloperViewSet.as_view({'get': 'retrieve'})),
    path('publisher', PublisherViewSet.as_view({'get': 'list'})),
    path('publisher/<int:pk>', PublisherViewSet.as_view({'get': 'retrieve'})),
    path('genres', GenresViewSet.as_view({'get': 'list'})),
    path('genres/<int:pk>', GenresViewSet.as_view({'get': 'retrieve'})),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

])
