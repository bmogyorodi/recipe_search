from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from django import forms

from data.models import Recipe
from data.models import Ingredient


def home(request):
    search_exp = request.GET.get("q", default="")

    included_ingr_str = request.GET.get("include", default="")
    included_ingr = [] if included_ingr_str == "" else included_ingr_str.split(",")

    excluded_ingr_str = request.GET.get("exclude", default="")
    excluded_ingr = [] if excluded_ingr_str == "" else excluded_ingr_str.split(",")

    ingredients = ["Chicken", "Tomato", "Garlic", "Cheddar", "Salt", "Pepper", "Plain Flour"]

    recipes = [
        {
            "title": "Roast chicken with forty cloves of garlic",
            "source_name": "BBC Food",
            "source_favicon": "https://www.bbc.co.uk/favicon.ico",
            "ratings": 3,
            "image": "https://ichef.bbci.co.uk//food/ic/food_16x9_832/recipes/chicken_with_40_cloves_22211_16x9.jpg",
            "canonical_url": "https://www.bbc.co.uk/food/recipes/chicken_with_40_cloves_22211",
            "ingredients": [
                ("Shallots", False),
                ("Chicken", True),
                ("Lemon", False),
                ("Butter", False)
            ],
            "total_time": 60
        },
        {
            "title": "Easy Chicken Fajitas",
            "source_name": "BBC GoodFood",
            "source_favicon": "https://www.bbcgoodfood.com/favicon.ico",
            "ratings": 4,
            "image": "https://images.immediate.co.uk/production/volatile/sites/30/2020/08/chicken-fajitas-2-d7172f8.jpg",
            "canonical_url": "https://www.bbcgoodfood.com/recipes/easy-chicken-fajitas",
            "ingredients": [
                ("Red Onion", False),
                ("Smoked Paprika", True),
                ("Chicken Breasts", True),
                ("Red Chilli", False)
            ],
            "total_time": 25
        },
        {
            "title": "Roast chicken with forty cloves of garlic",
            "source_name": "BBC Food",
            "source_favicon": "https://www.bbc.co.uk/favicon.ico",
            "ratings": None,
            "image": "https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/how_to_make_roast_71135_16x9.jpg",
            "canonical_url": "https://www.bbc.co.uk/food/recipes/how_to_make_roast_71135",
            "ingredients": [
                ("Shallots", False),
                ("Chicken", True),
                ("Lemon", False),
                ("Butter", False)
            ],
            "total_time": None
        }
    ]

    paginator = Paginator(recipes, 2)
    page_number = request.GET.get('page', default=1)
    page = paginator.get_page(page_number)

    context = {
        "page": page,
        "ingredients": ingredients,
        "search_params": {
            "search_exp": search_exp,
            "included_ingr": included_ingr,
            "excluded_ingr": excluded_ingr
        }
    }

    return render(request, 'core/index.html', context)
