from ._generic import RootSitemapScraper


class ACoupleCooksScraper(RootSitemapScraper):
    """
    A scraper for acouplecooks.com
    """

    NAME = "acouplecooks"
    RECIPE_URL_FORMAT = "https://www.acouplecooks.com/{id}/"
    # e.g. https://www.acouplecooks.com/easy-mint-water-recipe/ (no distinction)
    RECIPE_URL_RE = r"https://www.acouplecooks.com/(?P<id>[^/]+)/?$"

    SITEMAPS_ROOT_URL = "https://www.acouplecooks.com/sitemap_index.xml"
    SITEMAP_URL_RE = r"https://www.acouplecooks.com/post-sitemap(\d*).xml"
