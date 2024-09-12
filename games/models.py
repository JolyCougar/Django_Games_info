from datetime import date

from django.db import models
from django.urls import reverse


def game_poster_directory_path(instance: "Game", filename: str) -> str:
    return "game/{pk}/poster/{filename}".format(
        pk=instance.name,
        filename=filename,
    )


def logo_directory_path(instance: "Publisher", filename: str) -> str:
    return "logo_company/{pk}/{filename}".format(
        pk=instance.name,
        filename=filename,
    )


class Genres(models.Model):
    name = models.CharField("name", max_length=30)
    description = models.TextField("Description", null=True)
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self) -> str:
        return self.name


class GamePlatform(models.Model):
    name = models.CharField("name", max_length=30)

    def __str__(self) -> str:
        return self.name


class Developer(models.Model):
    name = models.CharField("name", max_length=30)
    logo = models.ImageField("Logo", upload_to=logo_directory_path, null=True)
    description = models.TextField("Description", null=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('developer_detail', kwargs={"slug": self.name})


class Publisher(models.Model):
    name = models.CharField("name", max_length=30)
    logo = models.ImageField("Logo", upload_to=logo_directory_path, null=True)
    description = models.TextField("Descriptions", null=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('publisher_detail', kwargs={"slug": self.name})


class Game(models.Model):
    name = models.CharField("name", max_length=100)
    description = models.TextField("Description", null=True)
    poster = models.ImageField("Poster", upload_to=game_poster_directory_path, null=True)
    release = models.DateField("Release game", default=date.today, null=True)
    game_platform = models.ManyToManyField(GamePlatform, null=True)
    url = models.SlugField(max_length=130, unique=True)
    publisher = models.ManyToManyField(Publisher, verbose_name="publisher", null=True, related_name="game_publisher")
    developer = models.ManyToManyField(Developer, verbose_name="developer", null=True, related_name="game_developer")
    genres = models.ManyToManyField(Genres, verbose_name="genres", null=True)
    draft = models.BooleanField("Draft", default=False)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("game_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.review_set.filter(parent__isnull=True)

    @property
    def description_short(self) -> str:
        if len(self.description) < 30:
            return self.description
        return self.description[:30] + "..."


def game_images_directory_path(instance: "GamesImages", filename: str) -> str:
    return "games/{pk}/images/{filename}".format(
        pk=instance.game.name,
        filename=filename,
    )


class GamesImages(models.Model):
    """ Images from Game """
    title = models.CharField("Title", max_length=100, null=True)
    description = models.TextField("Description", null=True)
    image = models.ImageField("Image", upload_to=game_images_directory_path)
    game = models.ForeignKey(Game, verbose_name="Game", on_delete=models.CASCADE)


class RatingStar(models.Model):
    """ Rating star """
    value = models.PositiveSmallIntegerField("Value", default=0)

    def __str__(self) -> str:
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
                               blank=True)
    game = models.ForeignKey(Game, verbose_name="Game", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} - {self.game}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
