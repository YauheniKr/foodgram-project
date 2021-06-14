from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet, 'ingredient_list')

urlpatterns = [
    path('', include(router.urls)),
]
