from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, SubscriptionViewSet, FavoriteViewSet,
                    PurchaseViewSet)

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet, 'ingredient_list')
router.register(r'subscriptions', SubscriptionViewSet, 'subscriptions')
router.register(r'favorites', FavoriteViewSet, 'favorites')
router.register(r'purchases', PurchaseViewSet, 'purchases')

urlpatterns = [
    path('v1/', include(router.urls)),
]
