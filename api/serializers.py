from rest_framework import serializers

from recipes.models import Unit, Ingredient, Follow, Favorite


class IngredientSerializer(serializers.ModelSerializer):
    unit = serializers.SlugRelatedField(slug_field='dimension',
                                        read_only=True)

    class Meta:
        fields = '__all__'
        model = Ingredient


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['author']
        model = Follow


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['recipe']