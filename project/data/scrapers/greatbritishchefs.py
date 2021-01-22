from ._generic import SitemapScraper


class GreatBritishChefsScraper(SitemapScraper):
    """
    A scraper for www.greatbritishchefs.com
    """

    NAME = "greatbritishchefs"
    RECIPE_URL_FORMAT = "https://www.greatbritishchefs.com/recipes/{id}/"
    RECIPE_URL_RE = r"https://www.greatbritishchefs.com/recipes/(?P<id>[^/]+)$"

    SITEMAP_URL = "https://www.greatbritishchefs.com/sitemap.xml"