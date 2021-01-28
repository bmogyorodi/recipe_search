from ._generic import RootSitemapScraper


class BonAppetitScraper(RootSitemapScraper):
    """
    A scraper for bonappetit.com
    """

    NAME = "bonappetit"
    RECIPE_URL_FORMAT = "https://www.bonappetit.com/recipe/{id}"
    # e.g. https://www.bonappetit.com/recipe/chicken-and-bread-salad-with-a-caper-vinaigrette
    RECIPE_URL_RE = r"https://www.bonappetit.com/recipe/(?P<id>[^/]+)/?$"

    SITEMAPS_ROOT_URL = "https://www.bonappetit.com/sitemap.xml"
    SITEMAP_URL_RE = r"https://www.bonappetit.com/sitemap.xml\?year=\d{4}&month=\d{1,2}&week=\d"
