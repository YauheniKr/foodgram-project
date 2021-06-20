from django.urls import path, include
from .views import (HomePage, AddRecipePage, DetailRecipePage, EditRecipePage,
                    ListFollowingPage, ListRecipeAuthorPage)

urlpatterns = [
    path('', HomePage.as_view(), name='index'),
    path('add/', AddRecipePage.as_view(), name='add_recipe'),
    path('detail/<int:pk>/', DetailRecipePage.as_view(), name='detail_recipe'),
    path('update/<int:pk>/', EditRecipePage.as_view(), name='update_recipe'),
    path('follow/', ListFollowingPage.as_view(), name='follow'),
    path('author/<int:pk>/', ListRecipeAuthorPage.as_view(), name='author_page')

]