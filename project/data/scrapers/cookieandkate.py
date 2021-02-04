from ._generic import SitemapScraper


class CookieAndKateScraper(SitemapScraper):
    """
    A scraper for cookieandkate.com
    """

    NAME = "cookieandkate"
    RECIPE_URL_FORMAT = "https://cookieandkate.com/{id}/"
    RECIPE_URL_RE = r"https://cookieandkate.com/(?P<id>[^/]+)/?$"

    SITEMAP_URL = "https://cookieandkate.com/post-sitemap.xml"
