from ._generic import RootSitemapScraper


class TasteScraper(RootSitemapScraper):
    """
    A scraper for taste.com.au
    """

    NAME = "taste"
    RECIPE_URL_FORMAT = "https://www.taste.com.au/recipes/{id}"
    RECIPE_URL_RE = r"https://www.taste.com.au/recipes/(?P<id>[^/]+/[^/]+)/?$"

    SITEMAPS_ROOT_URL = "https://www.taste.com.au/sitemap.xml"
    SITEMAP_URL_RE = r"https://www.taste.com.au/sitemap\d.xml"

    WILD_MODE = True
