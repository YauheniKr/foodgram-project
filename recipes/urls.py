from django.urls import path, include
from .views import HomePage, AddRecipePage #recipe_new

urlpatterns = [
    path('', HomePage.as_view(), name='index'),
    path('add/', AddRecipePage.as_view(), name='add_recipe')
]