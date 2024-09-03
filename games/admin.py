from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (Game, GamePlatform,
                     Genres, Rating, Review,
                     RatingStar, Developer, Publisher,
                     GamesImages)


class GamesImagesInLine(admin.TabularInline):
    model = GamesImages
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="120" height="120"')

    get_image.short_description = "Image"


class ReviewInline(admin.TabularInline):
    """ Reviews on game page"""
    model = Review
    extra = 1
    readonly_fields = ("name", "email")


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ("name", "url")


@admin.register(GamePlatform)
class GamePlatformAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "draft")
    list_filter = ("name", "game_platform",)
    search_fields = ("name", "genres__name",)
    list_editable = ("draft",)
    actions = ["published", "unpublished"]
    inlines = [GamesImagesInLine, ReviewInline]


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
    list_display = ("name", "email", "parent", "game", "id")
    readonly_fields = ("name", "email")


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    """ Create rating star """
    list_display = ("value",)


@admin.register(GamesImages)
class GamesImagesAdmin(admin.ModelAdmin):
    """ Images from Game """
    list_display = ("title", "game", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "image"
