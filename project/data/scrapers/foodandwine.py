from ._generic import RootSitemapScraper


class FoodAndWineScraper(RootSitemapScraper):
    """
    A scraper for foodandwine.com
    """

    NAME = "foodandwine"
    RECIPE_URL_FORMAT = "https://www.foodandwine.com/recipes/{id}"
    RECIPE_URL_RE = r"https://www.foodandwine.com/recipes/(?P<id>[^/]+)/?$"

    SITEMAPS_ROOT_URL = "https://www.foodandwine.com/sitemap.xml"
    SITEMAP_URL_RE = r"https://www.foodandwine.com/sitemaps/recipe/(\d+)/sitemap.xml"
