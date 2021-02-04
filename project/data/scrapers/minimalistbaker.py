from ._generic import RootSitemapScraper


class MinimalistBakerScraper(RootSitemapScraper):
    """
    A scraper for minimalistbaker.com
    """

    NAME = "minimalistbaker"
    RECIPE_URL_FORMAT = "https://minimalistbaker.com/{id}/"
    RECIPE_URL_RE = r"https://minimalistbaker.com/(?P<id>[^/]+)/?$"

    SITEMAPS_ROOT_URL = "https://minimalistbaker.com/sitemap_index.xml"
    SITEMAP_URL_RE = r"https://minimalistbaker.com/post-sitemap(\d+).xml"
