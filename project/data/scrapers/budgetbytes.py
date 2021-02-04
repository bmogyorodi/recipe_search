from ._generic import RootSitemapScraper


class BudgetBytesScraper(RootSitemapScraper):
    """
    A scraper for budgetbytes.com
    """

    NAME = "budgetbytes"
    RECIPE_URL_FORMAT = "https://www.budgetbytes.com/{id}"
    RECIPE_URL_RE = r"https://www.budgetbytes.com/(?P<id>[^/]+)/?$"

    SITEMAPS_ROOT_URL = "https://www.budgetbytes.com/sitemap_index.xml"
    SITEMAP_URL_RE = r"https://www.budgetbytes.com/post-sitemap\d.xml"
