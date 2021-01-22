from ._generic import RootSitemapScraper


class EatSmarterScraper(RootSitemapScraper):
    """
    A scraper for eatsmarter.com
    """

    NAME = "eatsmarter"
    RECIPE_URL_FORMAT = "https://eatsmarter.com/recipes/{id}"
    RECIPE_URL_RE = r"https://eatsmarter.com/recipes/(?P<id>[^/]+)$"

    SITEMAPS_ROOT_URL = "https://eatsmarter.com/sitemap.xml"
    SITEMAP_URL_RE = r"https://eatsmarter.com/sites/default/files/eatsmarter_sitemap/en/sitemap_(\d)+.xml"
