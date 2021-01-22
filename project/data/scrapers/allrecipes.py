from ._generic import RootSitemapScraper


class AllRecipesScraper(RootSitemapScraper):
    """
    A scraper for allrecipes.com
    """

    NAME = "allrecipes"
    RECIPE_URL_FORMAT = "https://www.allrecipes.com/recipe/{id}/"
    RECIPE_URL_RE = r"https://www.allrecipes.com/recipe/(?P<id>\d+).*"

    SITEMAPS_ROOT_URL = "https://www.allrecipes.com/sitemap.xml"
    SITEMAP_URL_RE = r"https://www.allrecipes.com/sitemaps/recipe/(\d+)/sitemap.xml"
