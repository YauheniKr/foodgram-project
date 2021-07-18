from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.shortcuts import HttpResponse, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, View)

from .forms import RecipeForm
from .models import Recipe, User
from .utils import edit_recipe, get_ingredients, get_request_tags, save_recipe


class HomePage(ListView):
    template_name = 'index.html'
    context_object_name = 'recipes'
    paginate_by = 6

    def get_queryset(self):
        tags = get_request_tags(self.request)
        recipes = Recipe.objects.filter(tags__title__in=tags).select_related(
            'author').prefetch_related('tags').distinct()
        return recipes

    def get_context_data(self, **kwargs):
        tags = get_request_tags(self.request)
        context = super().get_context_data(**kwargs)
        context['tags'] = tags
        return context


class AddRecipePage(LoginRequiredMixin, CreateView):
    template_name = 'formRecipe.html'
    form_class = RecipeForm

    def form_valid(self, form):
        try:
            ingredients = get_ingredients(self.request.POST)
        except forms.ValidationError as error:
            form.errors.update({'ingredients': error.message})
            return self.form_invalid(form)
        save_recipe(self.request, ingredients, form)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class DetailRecipePage(DetailView):
    context_object_name = 'recipe'
    model = Recipe
    template_name = 'singlePage.html'


class EditRecipePage(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    template_name = 'formRecipe.html'
    context_object_name = 'recipe'
    fields = ('title', 'image', 'text', 'cooking_time', 'tags',)
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        instance = self.get_object()
        try:
            edit_recipe(self.request, form, instance)
        except forms.ValidationError as error:
            form.errors.update({'ingredients': error.message})
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        args = self.kwargs["pk"]
        success_url = reverse_lazy('detail_recipe', args=[args])
        return success_url

    def test_func(self):
        obj = self.get_object()
        return obj.author == (self.request.user
                              or self.request.user.is_superuser)


class DeleteRecipePage(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Recipe
    pk_url_kwarg = 'pk'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def test_func(self):
        obj = self.get_object()
        return obj.author == (self.request.user
                              or self.request.user.is_superuser)


class ListFollowingPage(LoginRequiredMixin, View):

    def get(self, request):
        authors = (User.objects.filter(following__user=self.request.user).
                   prefetch_related('recipes').order_by('username').
                   annotate(recipe_count=Count('recipes')))
        paginator = Paginator(authors, 10)
        page_number = self.request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request, 'myFollow.html', {'authors': authors,
                                                 'page': page,
                                                 'paginator': paginator})


class ListRecipeAuthorPage(ListView):
    template_name = 'authorRecipe.html'
    context_object_name = 'recipes'
    paginate_by = 6

    def get_queryset(self):
        tags = get_request_tags(self.request)
        author = self.kwargs.get('pk')
        recipes = Recipe.objects.filter(tags__title__in=tags,
                                        author=author).select_related(
            'author').prefetch_related('tags').distinct()
        return recipes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = get_request_tags(self.request)
        author = self.kwargs.get('pk')
        author_recipes = get_object_or_404(User, id=author)
        context['tags'] = tags
        context['author'] = author_recipes
        return context


class ListFavoritePage(LoginRequiredMixin, ListView):
    template_name = 'favorite.html'
    context_object_name = 'recipes'
    paginate_by = 6

    def get_queryset(self):
        tags = get_request_tags(self.request)
        recipes = Recipe.objects.filter(
            favorite_by__user=self.request.user, tags__title__in=tags
        ).select_related('author').prefetch_related('tags').distinct()
        return recipes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = get_request_tags(self.request)
        context['tags'] = tags
        return context


class ListPurchasePage(LoginRequiredMixin, ListView):
    template_name = 'shopList.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        recipes = self.request.user.purchase_by.all()
        return recipes


class DownloadPurchasePage(LoginRequiredMixin, ListView):

    def get_queryset(self):
        title = 'recipe__ingredients__title'
        dimension = 'recipe__ingredients__unit__dimension'
        quantity = 'recipe__ingredients_amounts__quantity'
        ingredients = (self.request.user.purchase_by.select_related('recipe').
                       order_by(title).values(title, dimension).
                       annotate(amount=Sum(quantity)).all())
        return ingredients

    def render_to_response(self, context, **response_kwargs):
        title = 'recipe__ingredients__title'
        dimension = 'recipe__ingredients__unit__dimension'
        text = 'Список покупок:\n\n'
        for number, ingredient in enumerate(context.get('object_list'),
                                            start=1):
            amount = ingredient['amount']
            text += (
                f'{number}) '
                f'{ingredient[title]} - '
                f'{amount} '
                f'{ingredient[dimension]}\n'
            )

        response = HttpResponse(text, content_type='text/plain')
        filename = 'shopping_list.txt'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
