from rest_framework import serializers

from .models import Game, Review, Rating, Publisher, Developer


class FilterReviewListSerializer(serializers.ListSerializer):
    """ Filter reviews, only parent """

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """ Out recursive children """

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class DeveloperListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ("id", "name", "logo")


class PublisherListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ("id", "name", "logo")


class DeveloperDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = "__all__"


class PublisherDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = "__all__"


class GamesListSerializer(serializers.ModelSerializer):
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = Game
        fields = ("id", "name", "developer", "publisher", "description_short", "rating_user", "middle_star")


class ReviewCreateSerializer(serializers.ModelSerializer):
    """ Add review """

    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """ View review """
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("name", "text", "children")


class GameDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    publisher = PublisherListSerializer(read_only=True, many=True)
    developer = DeveloperListSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Game
        exclude = ("draft",)


class CreateRatingSerializer(serializers.ModelSerializer):
    """ Add Rating to game from user """

    class Meta:
        model = Rating
        fields = ("star", "game")

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('game', None),
            defaults={'star': validated_data.get('star')}
        )

        return rating
