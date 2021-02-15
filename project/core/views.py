from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
# from dal_select2 import views as autocomplete
# from dal_select2 import widgets
from django import forms

from data.models import Recipe
from data.models import Ingredient

ingredients_list = [
    Ingredient(title='cheese'),
    Ingredient(title='pepper'),
    Ingredient(title='tomato'),
    Ingredient(title='salt'),
    Ingredient(title='cucumber'),
    Ingredient(title='flour'),
    Ingredient(title='chicken breast'),
    Ingredient(title='chicken wings'),
    Ingredient(title='chicken fillet')
]
""" 
class IngredientAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs=Ingredient.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
class IngredientForm(forms.ModelForm):
    ingredient=forms.ModelChoiceField(
        queryset=Ingredient.objects.all(),
        widget=widgets.ModelSelect2(url='ingredient-autocomplete')
    )

    class Meta:
        model=Ingredient
        fields('__all__')
"""


def home(request):
    #recipe_list=Recipe.objects.all()
    recipe_list = [
        Recipe(title="Hamburger",
        image="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/beef_burger_with_98749_16x9.jpg",
        canonical_url= "https://www.bbc.co.uk/food/recipes/beef_bourguignon_with_89401",
        ratings=3.2),
        Recipe(title="Bagels",
        image="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/bagels_47163_16x9.jpg",
        canonical_url= "https://www.bbc.co.uk/food/recipes/beef_bourguignon_with_89401",
        ratings=5.0,
        ),
         Recipe(title="Hamburger",
        image="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/beef_burger_with_98749_16x9.jpg",
        canonical_url= "https://www.bbc.co.uk/food/recipes/beef_bourguignon_with_89401",
        ratings=3.2,),
        Recipe(title="Bagels",
        image="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/bagels_47163_16x9.jpg",
        canonical_url= "https://www.bbc.co.uk/food/recipes/beef_bourguignon_with_89401",
        ratings=5.0,
        ),
         Recipe(title="Hamburger",
        image="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/beef_burger_with_98749_16x9.jpg",
        canonical_url= "https://www.bbc.co.uk/food/recipes/beef_bourguignon_with_89401",
        ratings=3.2,),
        Recipe(title="Bagels",
        image="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/bagels_47163_16x9.jpg",
        canonical_url= "https://www.bbc.co.uk/food/recipes/beef_bourguignon_with_89401",
        ratings=5.0,
        ),
        Recipe(title="Hamburger",
        image="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/beef_burger_with_98749_16x9.jpg",
        canonical_url= "https://www.bbc.co.uk/food/recipes/beef_bourguignon_with_89401",
        ratings=3.2),
        Recipe(title="Bagels",
        image="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/bagels_47163_16x9.jpg",
        canonical_url= "https://www.bbc.co.uk/food/recipes/beef_bourguignon_with_89401",
        ratings=5.0,
        ),
    ] #test data

    search_exp=""
    if 'search_field' in request.GET:
        search_exp = request.GET['search_field']
    # pagination determines how many search results are on one page.
    paginator = Paginator(recipe_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/index.html',{'page_obj': page_obj, 'results_count':len(recipe_list),'search_exp':search_exp,'ingredients':ingredients_list},)
