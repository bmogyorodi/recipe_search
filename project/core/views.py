from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import When, Case, DecimalField

from data.models import Recipe, Ingredient
from data.search import recipe_search

from time import time


# TODO: change to actual ingredients and tags
search_ingredients = ["Onion", "Parmesan", "Chicken", "Tomato",
                      "Garlic", "Cheddar", "Salt", "Pepper", "Plain Flour"]
search_tags = ["Spanish", "Greek", "Italian",
               "Mexican", "British", "Polish", "German"]


def home(request):
    # Retrieve 3 recipes at random to display as suggestions
    recipes = Recipe.objects.all().order_by("?")[:3]

    context = {
        "recipes": recipes,
        "ingredients": search_ingredients,
        "search_params": {"included_ingr": [],
                          "excluded_ingr": [],
                          "must_have": []}
    }

    return render(request, 'core/home.html', context=context)


def search(request):
    search_exp = request.GET.get("q", default="").replace("+", " ")
    page_number = request.GET.get('page', default=1)

    included_ingr_str = request.GET.get("include", default="")
    included_ingr = [] if included_ingr_str == "" else included_ingr_str.split(
        ",")
    excluded_ingr_str = request.GET.get("exclude", default="")
    excluded_ingr = [] if excluded_ingr_str == "" else excluded_ingr_str.split(
        ",")
    must_have_ingr_str = request.GET.get("musthave", default="")
    must_have = [] if must_have_ingr_str == "" else must_have_ingr_str.split(
        ",")

    t_start = time()
    # If search is identical to the last (e.g. new page), use session instead
    if (
        len(request.session.get("recipe_pks", [])) > 0 and
        search_exp == request.session.get("search_exp") and
        included_ingr == request.session.get("included_ingr") and
        excluded_ingr == request.session.get("excluded_ingr") and
        must_have == request.session.get("must_have")
    ):
        res = [Recipe.objects.get(pk=pk)
               for pk in request.session["recipe_pks"]]
    else:
        res = recipe_search(query=search_exp,
                            include=included_ingr,
                            must_have=must_have,
                            exclude=excluded_ingr,
                            count=100)
        # Save found recipe PKs for quick loading next pages
        request.session["recipe_pks"] = [r.pk for r in res]
        # Save search parameters to determine a new search or not on next run
        request.session["search_exp"] = search_exp
        request.session["included_ingr"] = included_ingr
        request.session["excluded_ingr"] = excluded_ingr
        request.session["must_have"] = must_have

    total_time = f"Total time: {time() - t_start:.3f} seconds"
    paginator = Paginator(res, 10)

    page = paginator.get_page(page_number)

    context = {
        "page": page,
        "ingredients": search_ingredients,
        "tags": search_tags,
        "search_params": {
            "search_exp": search_exp,
            "included_ingr": included_ingr,
            "excluded_ingr": excluded_ingr,
            "must_have": must_have
        },
        "time": total_time,
        "result_count": len(res)
    }

    return render(request, 'core/search.html', context)
