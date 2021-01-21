from ._generic import Scraper
import requests
import xml.etree.ElementTree as ET
import re


class BBCFoodScraper(Scraper):
    """
    A scraper for bbc.co.uk/food
    """
    BASE_URL = "https://www.bbc.co.uk/food/recipes/{id}/"
    NAME = "bbcfood"
    SITEMAP_URL = "https://www.bbc.co.uk/food/sitemap.xml"

    def scrape_range(self, limit=None):
        regexp = re.compile(r"https://www.bbc.co.uk/food/recipes/(.+)")

        response = requests.get(self.SITEMAP_URL)
        root = ET.fromstring(response.content)

        ids = []

        for child in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
            url = child.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
            m = regexp.match(url)
            if m:
                ids.append(m.group(1))

        # Optional limit on the number of recipes to be scraped
        if limit:
            ids = ids[:limit]

        self.scrape_iterable(ids)
