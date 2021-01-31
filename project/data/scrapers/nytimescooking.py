from ._generic import RootSitemapScraper


class NYTimesCooking(RootSitemapScraper):
    """
    A scraper for cooking.nytimes.com
    """

    NAME = "nytimescooking"
    RECIPE_URL_FORMAT = "https://cooking.nytimes.com/recipes/{id}"
    RECIPE_URL_RE = r"https://cooking.nytimes.com/recipes/(?P<id>[^/]+)/?$"

    SITEMAPS_ROOT_URL = "https://www.nytimes.com/sitemaps/new/cooking.xml.gz"
    SITEMAP_URL_RE = r"https://www.nytimes.com/sitemaps/new/cooking-\d{4}-\d{2}.xml.gz"
