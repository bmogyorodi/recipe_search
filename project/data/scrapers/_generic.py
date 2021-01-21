from recipe_scrapers import scrape_me
from pathlib import Path
import time
import json


class Scraper():
    """
    A base Scraper class which implements essential methods for scraping general
    recipe websites.

    Each scraper should implement this class and set:
        - BASE_URL
        - NAME

    The rest will be handled by this abstract class
    """
    _DATA_DIR = Path(__file__).resolve().parent.parent / "data"
    _BASE_JSON = {
        # List of IDs that don't exist
        "dne": [],
        # Mapping of { id : recipe }
        "recipes": {},
    }

    # Format string, e.g., "https://www.allrecipes.com/recipe/{id}/"
    BASE_URL = NotImplemented
    # Without an extension, e.g. "allrecipes"
    NAME = NotImplemented
    # Save to DATA_FILE after N requests
    RECIPES_TO_SAVE = 10

    def __init__(self):
        # If data dir doesn't exist, create it
        self._DATA_DIR.parent.mkdir(parents=True, exist_ok=True)
        self.DATA_FILE = self._DATA_DIR / f"{self.NAME}.json"
        # Create the data file if it DNE
        if not self.DATA_FILE.exists():
            with open(self.DATA_FILE, "w") as f:
                json.dump(self._BASE_JSON, f)

    def _scrape_recipe(self, **kwargs):
        """
        Format url with **kwargs and return a recipe dict()
        """
        url = self.BASE_URL.format(**kwargs)
        scraper = scrape_me(url)

        # Empty title means HTTP 404
        if scraper.title() is None or scraper.title() == "":
            return None

        return self.scraper_to_recipe(scraper)

    def _save_to_datafile(self, data):
        with open(self.DATA_FILE, "w") as f:
            json.dump(data, f)

    def scraper_to_recipe(self, scraper):
        """
        Convert scraper object into a dict()
        """
        return {
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

    def scrape_iterable(self, iterable):
        """
        'iterable' must be an iterable, e.g.: list(), set(), range(), map()
        """
        with open(self.DATA_FILE, "r") as f:
            data = json.load(f)

        # Already scraped or don't exist
        dont_scrape = set(data["dne"]) | set(data["recipes"].keys())

        recipes_scraped = 0
        recipes_dne = 0
        recipes_skipped = 0
        t0 = time.time()
        for id in iterable:
            # Print progress
            total_time = time.time() - t0
            recipes_total = recipes_scraped + recipes_dne
            avg_time = 0 if recipes_total == 0 else total_time / \
                (recipes_total)
            print(f"Scraped: {recipes_scraped:<6} DNE: {recipes_dne:<6} "
                  f"Skipped: {recipes_skipped:<6} | "
                  f"Total: {total_time:>5.0f}s  AVG: {avg_time:>5.2f}s",
                  end="\r", flush=True)

            if id in dont_scrape:
                recipes_skipped += 1
                continue
            recipe = self._scrape_recipe(id=id)
            # No recipe returned -> doesn't exist
            if recipe is None:
                data["dne"].append(id)
                recipes_dne += 1
            else:
                data["recipes"][id] = recipe
                recipes_scraped += 1
            # Save every N recipes (even if DNE) so as not to lose progress
            if (recipes_scraped + recipes_dne) % self.RECIPES_TO_SAVE == 0:
                self._save_to_datafile(data)
        # Save everything at the end
        self._save_to_datafile(data)

        print("\n\n" + "-" * 30)
        print(f"Recipes scraped: {recipes_scraped}")
        print(f"Recipes DNE:     {recipes_dne}")
        total_time = time.time() - t0
        avg_time = total_time / (recipes_scraped + recipes_dne)
        print(f"Total time:      {total_time:.2f}s")
        print(f"Time/recipe:     {avg_time:.2f}s")

    class Meta:
        abstract = True
