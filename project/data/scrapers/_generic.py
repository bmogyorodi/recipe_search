from recipe_scrapers import scrape_me
from pathlib import Path
import logging
import time
import json
import re
import requests
import xml.etree.ElementTree as ET

log = logging.getLogger(__name__)


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

    # Name of scaper without an extension, e.g. "allrecipes"
    NAME = NotImplemented
    # Save to DATA_FILE after N requests
    RECIPES_TO_SAVE = 10
    # Format string, e.g., "https://www.allrecipes.com/recipe/{id}/"
    RECIPE_URL_FORMAT = NotImplemented
    # Regex with ?P<id> group which contains the ID of the recipe
    # e.g., r"https://www.allrecipes.com/recipe/(?P<id>\d+)/.*"
    RECIPE_URL_RE = NotImplemented

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
        url = self.RECIPE_URL_FORMAT.format(**kwargs)
        scraper = scrape_me(url)

        # Empty title means HTTP 404
        if scraper.title() is None or scraper.title() == "":
            return None

        try:
            return self.scraper_to_recipe(scraper)
        except Exception:
            log.exception(f"URL: {url} TITLE: {scraper.title()}")
            return None

    def _save_to_datafile(self, data):
        with open(self.DATA_FILE, "w") as f:
            json.dump(data, f)

    def scraper_to_recipe(self, scraper):
        """
        Convert scraper object into a dict()
        """
        obj = {
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
        try:
            obj["cuisine"] = scraper.cuisine()
        except AttributeError:
            obj["cuisine"] = scraper.schema.cuisine()
        return obj

    def scrape_iterable(self, iterable, overwrite=False):
        """
        'iterable' must be an iterable, e.g.: list(), set(), range(), map()
        """
        total_recipes = len(iterable)
        print(f"Total recipes to scrape: {total_recipes}")

        # Load previously scraped data
        with open(self.DATA_FILE, "r") as f:
            data = json.load(f)
        # Already scraped or don't exist; unless you want to overwrite
        if overwrite:
            dont_scrape = set(data["dne"])
        else:
            dont_scrape = set(data["dne"]) | set(data["recipes"].keys())

        recipes_scraped = 0
        recipes_dne = 0
        recipes_skipped = 0
        recipes_requests = 0
        t0 = time.time()
        for id in iterable:
            try:
                # Skip recipes that don't need to be scraped anymore
                if id in dont_scrape:
                    recipes_skipped += 1
                    continue

                recipe = self._scrape_recipe(id=id)
                recipes_requests += 1
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

                # Print progress
                total_time = time.time() - t0
                avg_time = total_time / recipes_requests
                recipes_remaining = total_recipes - (
                    recipes_scraped + recipes_dne + recipes_skipped)
                print(f" Scraped: {recipes_scraped:<6} DNE: {recipes_dne:<6} "
                      f"Skipped: {recipes_skipped:<6} "
                      f"Remaining: {recipes_remaining:<6} | "
                      f"Total: {total_time:>5.0f}s  AVG: {avg_time:>5.2f}s | "
                      f"ID: {id}",
                      end="\r", flush=True)
            except KeyboardInterrupt:
                self._save_to_datafile(data)
                print("\n")
                return
        # Save everything at the end
        self._save_to_datafile(data)

        print("\n\n" + "-" * 30)
        print(f"Recipes scraped: {recipes_scraped}")
        print(f"Recipes DNE:     {recipes_dne}")
        total_time = time.time() - t0
        print(f"Total time:      {total_time:.2f}s")
        if recipes_requests > 0:
            avg_time = total_time / recipes_requests
            print(f"Time/recipe:     {avg_time:.2f}s")

    class Meta:
        abstract = True


class SitemapScraper(Scraper):
    # Used for the XML tree traversal
    XML_ELEMENT_URL = "{http://www.sitemaps.org/schemas/sitemap/0.9}url"
    XML_ELEMENT_LOC = "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"

    # e.g., "https://www.bbc.co.uk/food/sitemap.xml"
    SITEMAP_URL = NotImplemented

    # Stores recipe IDs when running scrape_range to avoid unnecessary requests
    ids = None

    def get_ids_from_sitemap(self, url):
        """
        Retrieve a list of recipe IDs from a recipe sitemap
        'url' is a parameter because it's used in RootSitemapScraper
        """
        r = re.compile(self.RECIPE_URL_RE)
        res = requests.get(url)
        try:
            root = ET.fromstring(res.content)
        except ET.ParseError:
            log.exception(f"Sitemap URL: {url}")
            return []

        ids = []
        for el in root.findall(self.XML_ELEMENT_URL):
            recipe_url = el.find(self.XML_ELEMENT_LOC).text
            m = r.match(recipe_url)
            if m:
                ids.append(m.groupdict()["id"])
        return ids

    def get_all_ids(self):
        """
        Return a sorted list of all recipe IDs from the given sitemap
        """
        return sorted(self.get_ids_from_sitemap(self.SITEMAP_URL))

    def scrape_range(self, limit=None, overwrite=False):
        """
        Scrape some or all available recipe IDs
        """
        ids = self.get_all_ids()
        # Optional limit on the number of recipes to be scraped
        if limit:
            ids = ids[:limit]
        self.scrape_iterable(ids, overwrite=overwrite)


class RootSitemapScraper(SitemapScraper):
    # Not used, slightly different convention
    SITEMAP_URL = None

    # URL of the top-level sitemap with links to nested sitemaps
    SITEMAPS_ROOT_URL = NotImplemented
    # Regex which matches a URL to a nested sitemap, groups don't need names
    # e.g., r"https://www.allrecipes.com/sitemaps/recipe/(\d+)/sitemap.xml"
    SITEMAP_URL_RE = NotImplemented

    def get_sitemap_list(self):
        """
        Retrieves a list of sitemap URLs for the given root sitemap
        """
        r = re.compile(self.SITEMAP_URL_RE)
        res = requests.get(self.SITEMAPS_ROOT_URL)
        root = ET.fromstring(res.content)

        urls = []
        for sitemap in root.findall(
                "{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap"):
            url = sitemap.find(
                "{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
            m = r.match(url)
            if m:
                urls.append(url)
        return urls

    def get_all_ids(self, reload=False):
        """
        Return a sorted list of all recipe IDs from *all* recipe sitemaps
        If 'reload' is True, previously stored IDs will be ignored and reloaded
        """
        if self.ids is not None and not reload:
            return self.ids
        self.ids = []
        for sitemap in self.get_sitemap_list():
            self.ids.extend(self.get_ids_from_sitemap(sitemap))
        self.ids.sort()
        return self.ids
