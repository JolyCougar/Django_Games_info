from django.contrib import admin
from .models import Game, GamePlatform, Genres, Rating, Review, RatingStar, Developer, Publisher


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ("name", "url")


@admin.register(GamePlatform)
class GamePlatformAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("name", "game_platform", "url", "draft")
    list_filter = ("name", "game_platform",)
    search_fields = ("name", "genres__name",)
    list_editable = ("draft",)
    actions = ["published", "unpublished"]


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """ Rating """
    list_display = ("star", "game", "ip",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """ Reviews """
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ("value",)
