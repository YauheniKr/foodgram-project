from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .models import Recipe, Ingredient, Unit, Tag
from .forms import RecipeForm
from .utils import get_request_tags, save_recipe
from django.contrib.auth.mixins import LoginRequiredMixin


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
        context = super(HomePage, self).get_context_data(**kwargs)
        context['all_tags'] = Tag.objects.all()
        return context


class AddRecipePage(CreateView, LoginRequiredMixin):
    template_name = 'formRecipe.html'
    form_class = RecipeForm

    def form_valid(self, form):
        recipe = save_recipe(self.request, form)
        return super().form_valid(form)


class DetailRecipePage(DetailView):
    context_object_name = 'recipe'
    model = Recipe
    template_name = 'singlePage.html'


class EditRecipePage(UpdateView):
    model = Recipe
    template_name = 'singlePage.html'
    context_object_name = 'recipe'
    fields = ['title', ]
    pk_url_kwarg = 'pk'
