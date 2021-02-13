from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse

from data.models import Recipe


def home(request):
    recipe_list = [
        Recipe(title="Hamburger",
               image_url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/beef_burger_with_98749_16x9.jpg",
               canonical_url="https://www.bbc.co.uk/food/recipes/beef_bourguignon_with_89401",
               ratings=3.2,
               total_time=150,
               yields="4 serving(s)"),
        Recipe(title="Bagels",
               image_url="https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/bagels_47163_16x9.jpg",
               canonical_url="https://www.bbc.co.uk/food/recipes/beef_bourguignon_with_89401",
               ratings=5.0,
               total_time=120,
               yields="6 item(s)"
               ),


    ]  # test data
    search_exp = ""
    if 'search_field' in request.GET:
        search_exp = request.GET['search_field']
    # pagination determines how many search results are on one page.
    paginator = Paginator(recipe_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/index.html', {'page_obj': page_obj, 'results_count': len(recipe_list), 'search_exp': search_exp})

# Create your views here.
