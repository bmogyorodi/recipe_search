from ._generic import Scraper


class AllrecipesScraper(Scraper):
    """
    A scraper for allrecipes.com
    """
    BASE_URL = "https://www.allrecipes.com/recipe/{id}/"
    NAME = "allrecipes"

    def scrape_range(self, minimum, maximum):
        self.scrape_iterable(map(str, range(minimum, maximum + 1)))
