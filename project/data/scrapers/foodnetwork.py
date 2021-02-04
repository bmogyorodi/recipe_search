from ._generic import SitemapScraper


class FoodNetworkScraper(SitemapScraper):
    """
    A scraper for foodnetwork.co.uk
    """

    NAME = "foodnetwork"
    RECIPE_URL_FORMAT = "https://foodnetwork.co.uk/recipes/{id}/"
    RECIPE_URL_RE = r"https://foodnetwork.co.uk/recipes/(?P<id>[^/]+)/?$"

    SITEMAP_URL = "https://foodnetwork.co.uk/sitemap.xml"
