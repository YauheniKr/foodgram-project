from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, SubscriptionViewSet, FavoriteViewSet

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet, 'ingredient_list')
router.register(r'subscriptions', SubscriptionViewSet, 'subscriptions')
router.register(r'favorites', FavoriteViewSet, 'favorites')

urlpatterns = [
    path('', include(router.urls)),
]
