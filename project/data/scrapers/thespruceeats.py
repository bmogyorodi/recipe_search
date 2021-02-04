from ._generic import RootSitemapScraper

from recipe_scrapers.spruceeats import SpruceEats
from recipe_scrapers._utils import get_minutes, get_yields


class HotfixedSpruceEats(SpruceEats):
    def title(self):
        return self.soup.find("h1", {"class": "heading__title"}).text

    def author(self):
        container = self.soup.find("div", {"class": "article-byline"})
        if not container:
            return None
        author = container.find("span", {"class": "link__wrapper"})
        return author.text if author else None

    def total_time(self):
        return get_minutes(
            self.soup
            .find("div", {"class": "project-meta__total-time"})
            .find("span", {"class": "meta-text__data"})
        )

    def yields(self):
        return get_yields(
            self.soup.find(
                "div", {"class": "project-meta__recipe-serving"}).find(
                    "span", {"class": "meta-text__data"}
            ).text
        )

    def image(self):
        img = self.soup.find("img", {"class": "primary-image", "src": True})
        return img["src"] if img else None


class TheSpruceEatsScraper(RootSitemapScraper):
    """
    A scraper for thespruceeats.com
    """

    NAME = "thespruceeats"
    RECIPE_URL_FORMAT = "https://www.thespruceeats.com/{id}"
    # e.g. https://www.thespruceeats.com/white-bean-hummus-dip-3377730
    RECIPE_URL_RE = r"https://www.thespruceeats.com/(?P<id>[^/]+)/?$"

    SITEMAPS_ROOT_URL = "https://www.thespruceeats.com/sitemap.xml"
    SITEMAP_URL_RE = r"https://www.thespruceeats.com/sitemap_(\d+).xml"

    RECIPE_SCRAPER_CLASS = HotfixedSpruceEats
