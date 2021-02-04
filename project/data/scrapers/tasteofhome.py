from ._generic import RootSitemapScraper


class TasteOfHomeScraper(RootSitemapScraper):
    """
    A scraper for tasteofhome.com
    """

    NAME = "tasteofhome"
    RECIPE_URL_FORMAT = "https://www.tasteofhome.com/recipes/{id}/"
    # e.g. https://www.tasteofhome.com/recipes/tarver-tomato-gravy/
    RECIPE_URL_RE = r"https://www.tasteofhome.com/recipes/(?P<id>[^/]+)/?$"

    SITEMAPS_ROOT_URL = "https://www.tasteofhome.com/sitemap_index.xml"
    SITEMAP_URL_RE = r"https://www.tasteofhome.com/recipe-sitemap(\d+).xml"
