from datetime import date

from django.db import models


class GenresModel(models.Model):
    name = models.CharField("name", max_length=30)
    description = models.TextField("Description")
    url = models.SlugField(max_length=160, unique=True)


class GamePlatformModel(models.Model):
    name = models.CharField("name", max_length=30)


class DeveloperModel(models.Model):
    name = models.CharField("name", max_length=30)
    description = models.TextField("Description")


class PublisherModel(models.Model):
    name = models.CharField("name", max_length=30)
    description = models.TextField("Descriptions")


class GameModel(models.Model):
    name = models.CharField("name", max_length=100)
    description = models.TextField("Description")
    poster = models.ImageField("Poster", upload_to="games/")
    release = models.DateTimeField("Release game", default=date.today)
    game_platform = models.ForeignKey(GamePlatformModel, on_delete=models.CASCADE)
    url = models.SlugField(max_length=130, unique=True)
    publisher = models.ManyToManyField(PublisherModel)
    developer = models.ManyToManyField(DeveloperModel)
