from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse

from core.models import Recipe

def home(request):
    recipe_list = [
        Recipe(title="Hamburger",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/beef_burger_with_98749_16x9.jpg"),
        Recipe(title="Bagels",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/bagels_47163_16x9.jpg"),
        Recipe(title="Hamburger",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/beef_burger_with_98749_16x9.jpg"),
        Recipe(title="Bagels",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/bagels_47163_16x9.jpg"),
        Recipe(title="Hamburger",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/beef_burger_with_98749_16x9.jpg"),
        Recipe(title="Bagels",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/bagels_47163_16x9.jpg"),
        Recipe(title="Hamburger",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/beef_burger_with_98749_16x9.jpg"),
        Recipe(title="Bagels",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/bagels_47163_16x9.jpg"),
        Recipe(title="Hamburger",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/beef_burger_with_98749_16x9.jpg"),
        Recipe(title="Bagels",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/bagels_47163_16x9.jpg"),
        Recipe(title="Hamburger",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/beef_burger_with_98749_16x9.jpg"),
        Recipe(title="Bagels",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/bagels_47163_16x9.jpg"),
        Recipe(title="Hamburger",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/beef_burger_with_98749_16x9.jpg"),
        Recipe(title="Bagels",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/bagels_47163_16x9.jpg"),
        Recipe(title="Hamburger",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/beef_burger_with_98749_16x9.jpg"),
        Recipe(title="Bagels",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/bagels_47163_16x9.jpg"),
        Recipe(title="Hamburger",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/beef_burger_with_98749_16x9.jpg"),
        Recipe(title="Bagels",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/bagels_47163_16x9.jpg"),
        Recipe(title="Hamburger",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/beef_burger_with_98749_16x9.jpg"),
        Recipe(title="Bagels",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/bagels_47163_16x9.jpg"),
        Recipe(title="Hamburger",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/beef_burger_with_98749_16x9.jpg"),
        Recipe(title="Bagels",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/bagels_47163_16x9.jpg"),
        Recipe(title="Hamburger",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/beef_burger_with_98749_16x9.jpg"),
        Recipe(title="Bagels",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/bagels_47163_16x9.jpg"),
        Recipe(title="Hamburger",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/beef_burger_with_98749_16x9.jpg"),
        Recipe(title="Bagels",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/bagels_47163_16x9.jpg"),
        Recipe(title="Hamburger",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/beef_burger_with_98749_16x9.jpg"),
        Recipe(title="Bagels",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/bagels_47163_16x9.jpg"),
        Recipe(title="Hamburger",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/beef_burger_with_98749_16x9.jpg"),
        Recipe(title="Bagels",image_Url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/bagels_47163_16x9.jpg"),
    ] #test data
    paginator = Paginator(recipe_list, 3) #pagination determines how many search results are on one page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/index.html',{'page_obj': page_obj, 'results_count':len(recipe_list)})

# Create your views here.
