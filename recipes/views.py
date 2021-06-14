from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, ListView, CreateView
from .models import Recipe, Ingredient, Unit, Tag
from .forms import RecipeForm
from .utils import get_request_tags, save_recipe
from django.contrib.auth.decorators import login_required


class HomePage(ListView):
    template_name = 'index.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        tags = get_request_tags(self.request)
        recipes = Recipe.objects.filter(tags__title__in=tags).select_related(
            'author').prefetch_related('tags').distinct()
        return recipes


class AddRecipePage(CreateView):
    template_name = 'formRecipe.html'
    form_class = RecipeForm

    def form_valid(self, form):
        recipe = save_recipe(self.request, form)
        return super().form_valid(form)


"""@login_required
def recipe_new(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if form.is_valid():
        recipe = save_recipe(request, form)

        return redirect(
            reverse('index')
        )

    context = {'form': form}
    return render(request, 'formRecipe.html', context)"""


class ListRecipePage(ListView):
    pass
