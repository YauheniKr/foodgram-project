from rest_framework import serializers

from recipes.models import Unit, Ingredient, Follow


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
