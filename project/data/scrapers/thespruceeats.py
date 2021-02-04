from ._generic import RootSitemapScraper


class TheSpruceEatsScraper(RootSitemapScraper):
    """
    A scraper for thespruceeats.com
    """

    NAME = "thespruceeats"
    RECIPE_URL_FORMAT = "https://www.thespruceeats.com/{id}"
    # e.g. https://www.thespruceeats.com/white-bean-hummus-dip-3377730
    RECIPE_URL_RE = r"https://www.thespruceeats.com/(?P<id>[^/]+)/?$"

    SITEMAPS_ROOT_URL = "https://www.thespruceeats.com/sitemap.xml"
    SITEMAP_URL_RE = r"https://www.thespruceeats.com/sitemap_(\d+).xml"
