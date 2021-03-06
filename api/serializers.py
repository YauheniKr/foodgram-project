from rest_framework import serializers

from recipes.models import Favorite, Follow, Ingredient, Purchase


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


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['recipe']
