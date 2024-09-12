from modeltranslation.translator import register, TranslationOptions
from .models import Game, Publisher, Developer, Genres, GamesImages


@register(Game)
class GameTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(Publisher)
class PublisherTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(Developer)
class DeveloperTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(Genres)
class GenresTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(GamesImages)
class GamesImagesTranslationOptions(TranslationOptions):
    fields = ('description',)
