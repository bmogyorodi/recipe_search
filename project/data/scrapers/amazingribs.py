from ._generic import SitemapScraper


class AmazingRibsScraper(SitemapScraper):
    """
    A scraper for amazingribs.com
    """

    NAME = "amazingribs"
    RECIPE_URL_FORMAT = "https://amazingribs.com/tested-recipes/{id}/"
    # e.g. https://amazingribs.com/tested-recipes/duck-and-goose-recipes/grill-roasted-peking-duck-recipe
    # But NOT https://amazingribs.com/tested-recipes/duck-and-goose-recipes
    # So, the ID contains the category, otherwise could be ambiguous
    RECIPE_URL_RE = (
        r"https://amazingribs.com/tested-recipes/(?P<id>[^/]+/[^/]+)/?$"
    )

    SITEMAP_URL = "https://amazingribs.com/sitemap.xml"
