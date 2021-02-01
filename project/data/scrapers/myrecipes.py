from ._generic import RootSitemapScraper


class MyRecipesScraper(RootSitemapScraper):
    """
    A scraper for myrecipes.com
    """

    NAME = "myrecipes"
    RECIPE_URL_FORMAT = "https://www.myrecipes.com/recipe/{id}"
    RECIPE_URL_RE = r"https://www.myrecipes.com/recipe/(?P<id>[^/]+)/?$"

    SITEMAPS_ROOT_URL = "https://www.myrecipes.com/sitemap.xml"
    SITEMAP_URL_RE = r"https://www.myrecipes.com/sitemaps/recipe/\d/sitemap.xml"
