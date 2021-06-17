from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, SubscriptionViewSet

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet, 'ingredient_list')
router.register(r'subscriptions', SubscriptionViewSet, 'subscriptions')

urlpatterns = [
    path('', include(router.urls)),
]
