from ._generic import SitemapScraper


class GreatItalianChefsScraper(SitemapScraper):
    """
    A scraper for www.greatitalianchefs.com
    """

    NAME = "greatitalianchefs"
    RECIPE_URL_FORMAT = "https://www.greatitalianchefs.com/recipes/{id}/"
    RECIPE_URL_RE = r"https://www.greatitalianchefs.com/recipes/(?P<id>[^/]+)/?$"

    SITEMAP_URL = "https://www.greatitalianchefs.com/sitemap.xml"

    WILD_MODE = True
