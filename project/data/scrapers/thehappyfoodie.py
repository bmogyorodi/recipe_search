from ._generic import SitemapScraper


class TheHappyFoodieScraper(SitemapScraper):
    """
    A scraper for thehappyfoodie.co.uk
    """

    NAME = "thehappyfoodie"
    RECIPE_URL_FORMAT = "https://thehappyfoodie.co.uk/recipes/{id}/"
    RECIPE_URL_RE = r"https://thehappyfoodie.co.uk/recipes/(?P<id>[^/]+)/?$"

    SITEMAP_URL = "https://thehappyfoodie.co.uk/sitemap.xml"
