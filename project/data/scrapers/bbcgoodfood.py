from ._generic import RootSitemapScraper


class BBCGoodFoodScraper(RootSitemapScraper):
    """
    A scraper for bbcgoodfood.com
    """

    NAME = "bbcgoodfood"
    RECIPE_URL_FORMAT = "https://www.bbcgoodfood.com/recipes/{id}"
    # To avoid matching e.g.:
    # https://www.bbcgoodfood.com/recipes/collection/iceberg-lettuce-recipes
    RECIPE_URL_RE = r"https://www.bbcgoodfood.com/recipes/(?P<id>[^/]+)$"

    SITEMAPS_ROOT_URL = "https://www.bbcgoodfood.com/sitemap.xml"
    SITEMAP_URL_RE = r"https://www.bbcgoodfood.com/sitemap.xml\?yyyy=\d{4}&mm=\d{2}&dd=\d{2}"
