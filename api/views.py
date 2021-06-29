from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from recipes.models import Favorite, Follow, Ingredient, Purchase, Recipe, User

from .serializers import (FavoriteSerializer, IngredientSerializer,
                          PurchaseSerializer, SubscriptionSerializer)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class SubscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = SubscriptionSerializer
    queryset = Follow.objects.all()
    lookup_field = 'author'

    def perform_create(self, serializer):
        author = get_object_or_404(User, id=self.request.data.get('author'))
        serializer.save(user=self.request.user, author=author)

    def destroy(self, request, *args, **kwargs):
        author = get_object_or_404(User, id=kwargs.get('author'))
        instance = get_object_or_404(Follow, author=author, user=request.user)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()
    lookup_field = 'recipe'

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, id=self.request.data.get('recipe'))
        serializer.save(user=self.request.user, recipe=recipe)

    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs.get('recipe'))
        instance = get_object_or_404(Favorite, recipe=recipe, user=request.user)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PurchaseViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = PurchaseSerializer
    lookup_field = 'recipe'

    def get_queryset(self):
        return self.request.user.purchase_by.all()

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, id=self.request.data.get('recipe'))
        serializer.save(user=self.request.user, recipe=recipe)

    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs.get('recipe'))
        instance = get_object_or_404(Purchase, recipe=recipe,
                                     user=self.request.user)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
