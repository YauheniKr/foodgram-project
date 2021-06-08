from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Recipe


# Create your views here.
class HomePage(ListView):
    template_name = 'index.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        out = Recipe.objects.all()
        return out
