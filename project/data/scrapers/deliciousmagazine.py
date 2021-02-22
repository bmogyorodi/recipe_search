from ._generic import RootSitemapScraper


class DeliciousMagazineScraper(RootSitemapScraper):
    """
    A scraper for deliciousmagazine.co.uk
    """

    NAME = "deliciousmagazine"
    RECIPE_URL_FORMAT = "https://www.deliciousmagazine.co.uk/recipes/{id}"
    RECIPE_URL_RE = r"https://www.deliciousmagazine.co.uk/recipes/(?P<id>[^/]+)/?$"

    SITEMAPS_ROOT_URL = "https://www.deliciousmagazine.co.uk/sitemap_index.xml"
    SITEMAP_URL_RE = r"https://www.deliciousmagazine.co.uk/recipes-sitemap\d+.xml"

    WILD_MODE = True
