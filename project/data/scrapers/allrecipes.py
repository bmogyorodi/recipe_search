from recipe_scrapers import scrape_me
from pathlib import Path
from collections import OrderedDict
import time
import json

BASE_URL = "https://www.allrecipes.com/recipe/{id}/"
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "allrecipes.json"
BASE_JSON = {
    # List of IDs that don't exist
    "dne": [],
    "recipes": OrderedDict({}),
}
RECIPES_TO_SAVE = 50

# If data dir doesn't exist, create it
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)


def scrape_recipe(id):
    url = BASE_URL.format(id=id)
    scraper = scrape_me(url)

    # Empty title means HTTP 404
    if scraper.title() is None or scraper.title() == "":
        return None

    recipe = {
        "title": scraper.title(),
        "author": scraper.author(),
        "canonical_url": scraper.canonical_url(),
        "image": scraper.image(),
        "ingredients": scraper.ingredients(),
        "instructions": scraper.instructions(),
        "language": scraper.language(),
        "nutrients": scraper.nutrients(),
        "ratings": scraper.ratings(),
        "reviews": scraper.reviews(),
        "total_time": scraper.total_time(),
        "yields": scraper.yields(),
    }

    return recipe


def scrape_range(minimum, maximum):
    if not DATA_FILE.exists():
        data = BASE_JSON
    else:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

    # Already scraped or don't exist
    dont_scrape = set(data["dne"]) | set(data["recipes"].keys())

    recipes_scraped = 0
    recipes_dne = 0
    t0 = time.time()
    tx = time.time()
    for i in range(minimum, maximum + 1):
        id = str(i)
        if id in dont_scrape:
            continue
        recipe = scrape_recipe(id)
        # No recipe returned -> doesn't exist
        if recipe is None:
            data["dne"].append(id)
            recipes_dne += 1
        else:
            data["recipes"][id] = recipe
            recipes_scraped += 1
            # Save every N recipes so as not to lose progress
            if recipes_scraped % RECIPES_TO_SAVE == 0:
                with open(DATA_FILE, "w") as f:
                    json.dump(data, f)
                print(f"Scraped {RECIPES_TO_SAVE} recipes in "
                      f"{time.time()-tx:.2f}s")
                tx = time.time()
    # Save everything at the end
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

    print(f"Recipes scraped: {recipes_scraped}")
    print(f"Recipes DNE:     {recipes_dne}")
    total_time = time.time() - t0
    avg_time = total_time / (recipes_scraped + recipes_dne)
    print(f"Total time:      {total_time:.2f}s")
    print(f"Time/recipe:     {avg_time:.2f}s")
