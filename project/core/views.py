from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
#from dal_select2 import views as autocomplete
#from dal_select2 import widgets
from django import forms

from data.models import Recipe
from data.models import Ingredient

ingredients_list=[
        Ingredient(name='cheese',num_item=134),
        Ingredient(name='pepper',num_item=500),
        Ingredient(name='tomato',num_item=32),
        Ingredient(name='salt',num_item=400),
        Ingredient(name='cucumber',num_item=100),
        Ingredient(name='flour',num_item=330),
        Ingredient(name='chicken breast',num_item=400),
        Ingredient(name='chicken wings',num_item=300),
        Ingredient(name='chicken fillet',num_item=100)
    ]
""" class IngredientAutoComplete(autocomplete.Select2QuerySetView):
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
        fields('__all__')"""
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

# Create your views here.
