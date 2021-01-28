from ._generic import RootSitemapScraper


class ClaudiaAbrilScraper(RootSitemapScraper):
    """
    A scraper for claudia.abril.com.br
    """

    NAME = "claudiaabril"
    RECIPE_URL_FORMAT = "https://claudia.abril.com.br/receitas/{id}/"
    # e.g. https://claudia.abril.com.br/receitas/bolo-tres-leches/
    RECIPE_URL_RE = r"https://claudia.abril.com.br/receitas/(?P<id>[^/]+)/?$"

    SITEMAPS_ROOT_URL = "https://claudia.abril.com.br/sitemap.xml"
    SITEMAP_URL_RE = r"https://claudia.abril.com.br/sitemap.xml?\?yyyy=\d{4}&mm=\d{2}&dd=\d{2}"
