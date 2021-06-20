from django.shortcuts import render, redirect
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, \
    View
from .models import Recipe, Ingredient, Unit, Tag, Follow, User, Favorite
from .forms import RecipeForm
from .utils import get_request_tags, save_recipe, edit_recipe
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        UserPassesTestMixin)


class MyPaginator(Paginator):
    def validate_number(self, number):
        try:
            return super().validate_number(number)
        except EmptyPage:
            if int(number) > 1:
                # return the last page
                return self.num_pages
            elif int(number) < 1:
                # return the first page
                return 1
            else:
                raise


class HomePage(ListView):
    template_name = 'index.html'
    context_object_name = 'recipes'
    paginate_by = 6
    paginator_class = MyPaginator

    def get_queryset(self):
        tags = get_request_tags(self.request)
        recipes = Recipe.objects.filter(tags__title__in=tags).select_related(
            'author').prefetch_related('tags').distinct()
        return recipes

    def get_context_data(self, **kwargs):
        tags = get_request_tags(self.request)
        context = super(HomePage, self).get_context_data(**kwargs)
        context['all_tags'] = Tag.objects.all()
        context['tags'] = tags
        return context


class AddRecipePage(LoginRequiredMixin, CreateView):
    template_name = 'formRecipe.html'
    form_class = RecipeForm

    def form_valid(self, form):
        recipe = save_recipe(self.request, form)
        return super().form_valid(form)


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
        context = super(EditRecipePage, self).get_context_data(**kwargs)
        context['all_tags'] = Tag.objects.all()
        return context

    def form_valid(self, form):
        instance = Recipe.objects.get(id=self.kwargs["pk"])
        edit_recipe(self.request, form, instance)
        return super().form_valid(form)

    def get_success_url(self):
        args = self.kwargs["pk"]
        success_url = reverse_lazy('detail_recipe', args=[args])
        return success_url

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user or self.request.user.is_superuser


class ListFollowingPage(View):

    def get(self, request):
        authors = User.objects.filter(following__user=self.request.user). \
            prefetch_related('recipes').order_by('username'). \
            annotate(recipe_count=Count('recipes'))
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
    paginator_class = MyPaginator

    def get_queryset(self):
        tags = get_request_tags(self.request)
        author = self.kwargs.get('pk')
        recipes = Recipe.objects.filter(tags__title__in=tags,
                                        author=author).select_related(
            'author').prefetch_related('tags').distinct()
        return recipes

    def get_context_data(self, **kwargs):
        context = super(ListRecipeAuthorPage, self).get_context_data(**kwargs)
        tags = get_request_tags(self.request)
        context['all_tags'] = Tag.objects.all()
        context['tags'] = tags
        return context


class ListFavoritePage(ListView):
    template_name = 'favorite.html'
    context_object_name = 'recipes'
    paginate_by = 6
    paginator_class = MyPaginator

    def get_queryset(self):
        tags = get_request_tags(self.request)
        recipes = Recipe.objects.filter(
            favorite_by__user=self.request.user, tags__title__in=tags
        ).select_related('author').prefetch_related('tags').distinct()
        return recipes

    def get_context_data(self, **kwargs):
        context = super(ListFavoritePage, self).get_context_data(**kwargs)
        tags = get_request_tags(self.request)
        context['all_tags'] = Tag.objects.all()
        context['tags'] = tags
        return context
