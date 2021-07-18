from django.urls import path

from .views import (AddRecipePage, DeleteRecipePage, DetailRecipePage,
                    DownloadPurchasePage, EditRecipePage, HomePage,
                    ListFavoritePage, ListFollowingPage, ListPurchasePage,
                    ListRecipeAuthorPage)

urlpatterns = [
    path('', HomePage.as_view(), name='index'),
    path('add/', AddRecipePage.as_view(), name='add_recipe'),
    path('detail/<int:pk>/', DetailRecipePage.as_view(), name='detail_recipe'),
    path('update/<int:pk>/', EditRecipePage.as_view(), name='update_recipe'),
    path('delete/<int:pk>/', DeleteRecipePage.as_view(), name='delete_recipe'),
    path('follow/', ListFollowingPage.as_view(), name='follow'),
    path('author/<int:pk>/', ListRecipeAuthorPage.as_view(),
         name='author_page'),
    path('favoroties/<int:pk>', ListFavoritePage.as_view(),
         name='favorate_page'),
    path('purchases/', ListPurchasePage.as_view(),
         name='purchase_page'),
    path('download_purchases/', DownloadPurchasePage.as_view(),
         name='download_purchases')
]
