from ._generic import RootSitemapScraper


class AmbitiousKitchenScraper(RootSitemapScraper):
    """
    A scraper for ambitiouskitchen.com
    """

    NAME = "ambitiouskitchen"
    RECIPE_URL_FORMAT = "https://www.ambitiouskitchen.com/{id}/"
    # e.g. https://www.ambitiouskitchen.com/healthy-white-chicken-chili/
    # Recipes are not distinct from any other post, all have only a slug
    RECIPE_URL_RE = r"https://www.ambitiouskitchen.com/(?P<id>[^/]+)/?$"

    SITEMAPS_ROOT_URL = "https://www.ambitiouskitchen.com/sitemap.xml"
    SITEMAP_URL_RE = r"https://www.ambitiouskitchen.com/sitemap-pt-post-\d{4}-\d{2}.xml"
