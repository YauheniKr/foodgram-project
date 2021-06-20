from rest_framework import permissions, viewsets, filters, mixins
from rest_framework.decorators import permission_classes, action
from .serializers import IngredientSerializer, SubscriptionSerializer, FavoriteSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from recipes.models import Ingredient, Follow, User, Recipe, Favorite
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status


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
