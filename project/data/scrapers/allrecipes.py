import requests
import xml.etree.ElementTree as ET
import re
from ._generic import Scraper


class AllRecipesScraper(Scraper):
    """
    A scraper for allrecipes.com
    """
    BASE_URL = "https://www.allrecipes.com/recipe/{id}/"
    NAME = "allrecipes"

    SITEMAPS_ROOT_URL = "https://www.allrecipes.com/sitemap.xml"
    SITEMAP_URL_RE = r"https://www.allrecipes.com/sitemaps/recipe/(\d+)/sitemap.xml"
    RECIPE_URL_RE = r"https://www.allrecipes.com/recipe/(?P<id>\d+)/(?P<slug>.?)/?"

    ids = None

    def get_sitemap_list(self):
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

    def get_ids_from_sitemap(self, url):
        r = re.compile(self.RECIPE_URL_RE)
        res = requests.get(url)
        root = ET.fromstring(res.content)

        ids = []
        for el in root.findall(
                "{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
            recipe_url = el.find(
                "{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
            m = r.match(recipe_url)
            if m:
                ids.append(m.group(1))
        return ids

    def get_all_ids(self):
        ids = []
        for sitemap in self.get_sitemap_list():
            ids.extend(self.get_ids_from_sitemap(sitemap))
        return sorted(ids)

    def scrape_range(self, limit=None):
        if self.ids is None:
            self.ids = self.get_all_ids()
        # Optional limit on the number of recipes to be scraped
        if limit:
            ids = self.ids[:limit]
        else:
            ids = self.ids

        self.scrape_iterable(ids)
