from datetime import date

from django.db import models


def game_poster_directory_path(instance: "Game", filename: str) -> str:
    return "game/game_{pk}/poster/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Genres(models.Model):
    name = models.CharField("name", max_length=30)
    description = models.TextField("Description")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name


class GamePlatform(models.Model):
    name = models.CharField("name", max_length=30)

    def __str__(self):
        return self.name


class Developer(models.Model):
    name = models.CharField("name", max_length=30)
    description = models.TextField("Description")

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField("name", max_length=30)
    description = models.TextField("Descriptions")

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField("name", max_length=100)
    description = models.TextField("Description")
    poster = models.ImageField("Poster", upload_to=game_poster_directory_path)
    release = models.DateField("Release game", default=date.today)
    game_platform = models.ForeignKey(GamePlatform, on_delete=models.CASCADE)
    url = models.SlugField(max_length=130, unique=True)
    publisher = models.ManyToManyField(Publisher, verbose_name="publisher")
    developer = models.ManyToManyField(Developer, verbose_name="developer")
    genres = models.ManyToManyField(Genres, verbose_name="genres")
    draft = models.BooleanField("Draft", default=False)

    def __str__(self):
        return self.name


def game_images_directory_path(instance: "GamesImages", filename: str) -> str:
    return "games/game_{pk}/images/{filename}".format(
        pk=instance.game.pk,
        filename=filename,
    )


class GamesImages(models.Model):
    """ Images from Game """
    title = models.CharField("Title", max_length=100)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to=game_images_directory_path)
    game = models.ForeignKey(Game, verbose_name="Game", on_delete=models.CASCADE)


class RatingStar(models.Model):
    """ Rating star """
    value = models.PositiveSmallIntegerField("Value", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Rating Star"
        verbose_name_plural = "Rating Stars"
        ordering = ["-value"]


class Rating(models.Model):
    """ Rating """
    ip = models.CharField("IP", max_length=15)
    star = models.ForeignKey(RatingStar, verbose_name="Star", on_delete=models.CASCADE)
    game = models.ForeignKey(Game, verbose_name="Game", on_delete=models.CASCADE, related_name="ratings")

    def __str__(self):
        return f"{self.star} - {self.game}"

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"


class Review(models.Model):
    """ Reviews"""
    email = models.EmailField()
    name = models.CharField("Name", max_length=100)
    text = models.TextField("Text", max_length=5000)
    parent = models.ForeignKey("self", verbose_name="Parent",
                               on_delete=models.SET_NULL, null=True,
                               blank=True, related_name="children")
    movie = models.ForeignKey(Game, verbose_name="Movie", on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
