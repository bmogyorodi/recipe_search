from ._generic import RootSitemapScraper


class EpicuriousScraper(RootSitemapScraper):
    """
    A scraper for epicurious.com
    """

    NAME = "epicurious"
    RECIPE_URL_FORMAT = "https://www.epicurious.com/recipes/food/views/{id}"
    RECIPE_URL_RE = r"https://www.epicurious.com/recipes/food/views/(?P<id>[^/]+)/?$"

    SITEMAPS_ROOT_URL = "https://www.epicurious.com/sitemap.xml/editorial-recipes"
    SITEMAP_URL_RE = r"https://www.epicurious.com/sitemap.xml/editorial-recipes\?year=\d{4}&month=\d{1,2}&week=\d"
