from ._generic import SitemapScraper


class JamieOliverScraper(SitemapScraper):
    """
    A scraper for jamieoliver.com
    """

    NAME = "jamieoliver"
    RECIPE_URL_FORMAT = "https://www.jamieoliver.com/recipes/{id}/"
    # e.g. https://www.jamieoliver.com/recipes/vegetarian-recipes/creamy-paneer-veg-curry/
    # All recipes have a category assigned
    RECIPE_URL_RE = (
        r"https://www.jamieoliver.com/recipes/(?P<id>[^/]+/[^/]+)/?$"
    )

    SITEMAP_URL = "https://www.jamieoliver.com/recipes.xml"
