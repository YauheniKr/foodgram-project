from rest_framework import permissions, viewsets, filters, mixins
from rest_framework.decorators import permission_classes, action
from .serializers import IngredientSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from recipes.models import Ingredient


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']



