from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .models import Recipe, Ingredient, Unit, Tag
from .forms import RecipeForm
from .utils import get_request_tags, save_recipe, edit_recipe
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)


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
    paginate_by = 4
    paginator_class = MyPaginator

    def get_queryset(self):
        tags = get_request_tags(self.request)
        recipes = Recipe.objects.filter(tags__title__in=tags).select_related(
            'author').prefetch_related('tags').distinct()
        return recipes

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['all_tags'] = Tag.objects.all()
        page = self.request.GET.get('page', 1)
        recipes = HomePage.get_queryset(self)
        paginator = self.paginator_class(recipes, self.paginate_by)
        recipes = paginator.page(page)
        context['recipes'] = recipes
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


class EditRecipePage(LoginRequiredMixin, UpdateView):
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
