from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import When, Case, DecimalField

from data.models import Recipe, Source
from data.search import RankedSearch

from time import time


sample_recipes = [
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

sample_ingredients = ["Chicken", "Tomato", "Garlic",
                      "Cheddar", "Salt", "Pepper", "Plain Flour"]

sample_tags = ["Spanish", "Greek", "Italian",
               "Mexican", "British", "Polish", "German"]


def home(request):
    search_exp = request.GET.get("q", default="").replace("+", " ")
    use_fake_data = request.GET.get("fake_data", default="False")

    included_ingr_str = request.GET.get("include", default="")
    included_ingr = [] if included_ingr_str == "" else included_ingr_str.split(
        ",")

    excluded_ingr_str = request.GET.get("exclude", default="")
    excluded_ingr = [] if excluded_ingr_str == "" else excluded_ingr_str.split(
        ",")

    total_time = None
    res = []
    if use_fake_data == "True":
        paginator = Paginator(sample_recipes, 2)
    elif len(search_exp) > 0:
        t_start = time()
        scores = RankedSearch().search(search_exp)
        t_retrieval = time()

        # Obtain retrieved recipes, annotate with score, and order by it
        pks = [recipe_id for recipe_id, _ in scores[:100]]
        for pk in pks:
            res.append(Recipe.objects.get(pk=pk))
        # ? another way to order but takes 0.6s instead of 0.2s
        # whens = [When(pk=k, then=v) for k, v in scores]
        # res = Recipe.objects.filter(pk__in=pks).annotate(
        #     score=Case(*whens, default=0, output_field=DecimalField())
        # ).order_by('-score')

        t_data = time()

        total_time = (f"Retrieval: {t_retrieval - t_start:.4f}, "
                      f"Processing: {t_data -t_retrieval:.4f}, "
                      f"Total: {time() - t_start:.4f}")
        paginator = Paginator(res, 10)
    else:
        paginator = Paginator([], 10)

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

    return render(request, 'core/index.html', context)
