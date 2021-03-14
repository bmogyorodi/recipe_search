from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import When, Case, DecimalField

from data.models import Recipe
from data.search import recipe_search

from time import time


sample_ingredients = ["Chicken", "Tomato", "Garlic",
                      "Cheddar", "Salt", "Pepper", "Plain Flour"]

sample_tags = ["Spanish", "Greek", "Italian",
               "Mexican", "British", "Polish", "German"]


def home(request):
    # Retrieve 3 recipes at random to display as suggestions
    recipes = Recipe.objects.all().order_by("?")[:3]

    context = {
        "recipes": recipes
    }

    return render(request, 'core/home.html', context=context)


def search(request):
    search_exp = request.GET.get("q", default="").replace("+", " ")

    included_ingr_str = request.GET.get("include", default="")
    included_ingr = [] if included_ingr_str == "" else included_ingr_str.split(
        ",")

    excluded_ingr_str = request.GET.get("exclude", default="")
    excluded_ingr = [] if excluded_ingr_str == "" else excluded_ingr_str.split(
        ",")

    must_have_ingr_str = request.GET.get("must_have", default="")
    must_have = [] if must_have_ingr_str == "" else must_have_ingr_str.split(
        ",")

    total_time = None

    t_start = time()
    res = recipe_search(query=search_exp,
                        include=included_ingr,
                        must_have=must_have,
                        exclude=excluded_ingr,
                        count=100)
    t_retrieval = time()

    t_data = time()
    total_time = (f"Retrieval: {t_retrieval - t_start:.4f}, "
                  f"Processing: {t_data -t_retrieval:.4f}, "
                  f"Total: {time() - t_start:.4f}")
    paginator = Paginator(res, 10)

    page_number = request.GET.get('page', default=1)
    page = paginator.get_page(page_number)

    context = {
        "page": page,
        "ingredients": sample_ingredients,
        "tags": sample_tags,
        "search_params": {
            "search_exp": search_exp,
            "included_ingr": included_ingr,
            "excluded_ingr": excluded_ingr
        },
        "time": total_time,
        "result_count": len(res)
    }

    return render(request, 'core/search.html', context)
