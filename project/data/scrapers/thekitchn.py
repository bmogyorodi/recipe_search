from ._generic import RootSitemapScraper


class TheKitchnScraper(RootSitemapScraper):
    """
    A scraper for thekitchn.com
    """

    NAME = "thekitchn"
    RECIPE_URL_FORMAT = "https://www.thekitchn.com/{id}"
    # e.g. https://www.thekitchn.com/zucchini-muffins-pinch-of-yum-22939410
    RECIPE_URL_RE = r"https://www.thekitchn.com/(?P<id>[^/]+)/?$"

    SITEMAPS_ROOT_URL = "https://www.thekitchn.com/sitemap.xml"
    # e.g. https://www.thekitchn.com/sitemap-2021-01.xml
    SITEMAP_URL_RE = r"https://www.thekitchn.com/sitemap-\d{4}-\d{2}.xml"
