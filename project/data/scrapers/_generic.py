from recipe_scrapers import scrape_me, NoSchemaFoundInWildMode
from requests.exceptions import TooManyRedirects
from pathlib import Path
from datetime import timedelta
import logging
import time
import re
import requests
import xml.etree.ElementTree as ET
import bz2
import pickle

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
    RECIPES_TO_SAVE = 100
    # Format string, e.g., "https://www.allrecipes.com/recipe/{id}/"
    RECIPE_URL_FORMAT = NotImplemented
    # Regex with ?P<id> group which contains the ID of the recipe
    # e.g., r"https://www.allrecipes.com/recipe/(?P<id>\d+)/.*"
    RECIPE_URL_RE = NotImplemented
    # Whether wild mode is to be used for the scraper
    WILD_MODE = False
    # In case we need to hotfix a class from recipe_scrapers
    RECIPE_SCRAPER_CLASS = None
    # Request headers
    REQUEST_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0"}

    def __init__(self):
        # If data dir doesn't exist, create it
        self._DATA_DIR.parent.mkdir(parents=True, exist_ok=True)
        self.DATA_FILE = self._DATA_DIR / f"{self.NAME}.pbz2"
        # Create the data file if it DNE
        if not self.DATA_FILE.exists():
            self._save_to_datafile(self._BASE_JSON)

    def _scrape_recipe(self, **kwargs):
        """
        Format url with **kwargs and return a recipe dict()
        """
        url = self.RECIPE_URL_FORMAT.format(**kwargs)
        scraper = scrape_me(url, wild_mode=self.WILD_MODE)
        # If a custom class has been specified, always use it
        if self.RECIPE_SCRAPER_CLASS:
            scraper = self.RECIPE_SCRAPER_CLASS(url)
        else:
            scraper = scrape_me(url, wild_mode=self.WILD_MODE)

        # Empty title means HTTP 404 or e.g. category/recipe list
        if scraper.title() is None or scraper.title() == "":
            return None

        try:
            return self.scraper_to_recipe(scraper)
        except Exception:
            log.exception(f"URL: {url} TITLE: {scraper.title()}")
            return None

    def _save_to_datafile(self, data):
        with bz2.BZ2File(self.DATA_FILE, "wb") as f:
            pickle.dump(data, f)

    def load_from_datafile(self):
        with bz2.BZ2File(self.DATA_FILE, "rb") as f:
            return pickle.load(f)

    def scraper_to_recipe(self, scraper):
        """
        Convert scraper object into a dict()
        """
        obj = {
            "title": scraper.title(),
            "canonical_url": scraper.canonical_url(),
            "language": scraper.language(),
        }

        # e.g. GreatBritishChefs has no schema and doesn't implement author()
        def get_val_or_empty(scraper, attr):
            try:
                # scraper.author() always exists but depends on schema if it
                # isn't implemented on the non-abstract scraper
                return getattr(scraper, attr, lambda: "")()
            except (AttributeError, NotImplementedError):
                return ""
        obj["author"] = get_val_or_empty(scraper, "author")
        obj["image"] = get_val_or_empty(scraper, "image")
        obj["ingredients"] = get_val_or_empty(scraper, "ingredients")
        obj["instructions"] = get_val_or_empty(scraper, "instructions")
        obj["nutrients"] = get_val_or_empty(scraper, "nutrients")
        obj["ratings"] = get_val_or_empty(scraper, "ratings")
        obj["reviews"] = get_val_or_empty(scraper, "reviews")
        obj["total_time"] = get_val_or_empty(scraper, "total_time")
        obj["yields"] = get_val_or_empty(scraper, "yields")
        # Some scrapers might have schema with cuisine but cuisine() undefined
        try:
            obj["cuisine"] = scraper.cuisine()
        except AttributeError:
            obj["cuisine"] = get_val_or_empty(
                getattr(scraper, "schema", {}), "cuisine")
        return obj

    def scrape_iterable(self, iterable, overwrite=False):
        """
        'iterable' must be an iterable, e.g.: list(), set(), range(), map()
        """
        total_recipes = len(iterable)
        print(f"Total recipes available to scrape: {total_recipes}")

        # Load previously scraped data
        data = self.load_from_datafile()
        # Already scraped or don't exist; unless you want to overwrite
        if overwrite:
            dont_scrape = set(data["dne"])
        else:
            dont_scrape = set(data["dne"]) | set(data["recipes"].keys())

        print(f"Recipes already scraped: {len(data['recipes'])}")
        print(f"Recipes marked as DNE: {len(data['dne'])}")

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

                try:
                    recipe = self._scrape_recipe(id=id)
                except (NoSchemaFoundInWildMode, TooManyRedirects):
                    recipe = None
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
                total_delta = timedelta(seconds=round(total_time))
                avg_time = total_time / recipes_requests
                recipes_remaining = total_recipes - (
                    recipes_scraped + recipes_dne + recipes_skipped)
                estimated_delta = timedelta(
                    seconds=round(recipes_remaining * avg_time))
                print(f" Scraped: {recipes_scraped:<6} DNE: {recipes_dne:<6} "
                      f"Skipped: {recipes_skipped:<6} "
                      f"Remaining: {recipes_remaining:<6} | "
                      f"Total: {total_delta}  AVG: {avg_time:>5.2f}s  "
                      f"Estimated: {estimated_delta} | "
                      f"ID: {id}"
                      "\033[K",  # ANSI "erase to end of line"
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
        res = requests.get(url, headers=self.REQUEST_HEADERS)
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

    def get_all_ids(self, reload=False):
        """
        Return a sorted list of all recipe IDs from the given sitemap
        """
        if self.ids is not None and not reload:
            return self.ids
        self.ids = sorted(self.get_ids_from_sitemap(self.SITEMAP_URL))
        return self.ids

    def num_recipes(self):
        """
        Return the number of recipe *available to scrape*
        """
        return len(self.get_all_ids())

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
        res = requests.get(self.SITEMAPS_ROOT_URL, headers=self.REQUEST_HEADERS)
        try:
            root = ET.fromstring(res.content)
        except ET.ParseError:
            log.exception(f"ROOT Sitemap URL: {self.SITEMAPS_ROOT_URL}")
            return []
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
