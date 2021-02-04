from ._generic import SitemapScraper


class TescoRealFoodScraper(SitemapScraper):
    """
    A scraper for realfood.tesco.co.uk
    """

    NAME = "tescorealfood"
    RECIPE_URL_FORMAT = "https://realfood.tesco.com/recipes/{id}.html"
    RECIPE_URL_RE = r"https://realfood.tesco.com/recipes/(?P<id>[^/-][^/]+)\.html$"

    SITEMAP_URL = "https://realfood.tesco.com/sitemap.xml"

    WILD_MODE = True
