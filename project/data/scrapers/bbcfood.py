from ._generic import SitemapScraper


class BBCFoodScraper(SitemapScraper):
    """
    A scraper for bbc.co.uk/food
    """

    NAME = "bbcfood"
    RECIPE_URL_FORMAT = "https://www.bbc.co.uk/food/recipes/{id}/"
    RECIPE_URL_RE = r"https://www.bbc.co.uk/food/recipes/(?P<id>.+)"

    SITEMAP_URL = "https://www.bbc.co.uk/food/sitemap.xml"
