from ._generic import SitemapScraper


class TastyScraper(SitemapScraper):
    """
    A scraper for tasty.co
    """

    NAME = "tasty"
    RECIPE_URL_FORMAT = "https://tasty.co/recipe/{id}"
    RECIPE_URL_RE = r"https://tasty.co/recipe/(?P<id>[^/]+)/?$"

    SITEMAP_URL = "https://tasty.co/sitemaps/tasty/sitemap.xml"
