"""

#### List of available websites for scraping, thanks to recipe-scrapers ####

# Implemented
https://www.acouplecooks.com
https://allrecipes.com/
https://amazingribs.com/
https://ambitiouskitchen.com/
https://bbc.co.uk/
    https://bbc.com/ (redirects to bbc.co.uk for Food)
https://bbcgoodfood.com/
https://bonappetit.com/
https://claudia.abril.com.br/
https://eatsmarter.com/
https://epicurious.com/
https://greatbritishchefs.com/
https://cooking.nytimes.com/
https://tasty.co
https://thehappyfoodie.co.uk/


# Have a Sitemap
https://averiecooks.com/ (post-sitemap1.xml)
https://bakingmischief.com/ (post-sitemap.xml)
https://bettycrocker.com/ (AiO, at https://www.bettycrocker.com/recipe.xml, /recipes/{id}/{hash-like id})
https://bowlofdelicious.com/ (post-sitemap.xml)
https://budgetbytes.com/ (post-sitemap1.xml)


# Don't have a Sitemap, not interested
https://www.750g.com
https://archanaskitchen.com/
https://www.atelierdeschefs.fr/
https://blueapron.com/


# To be classified
https://cdkitchen.com/
https://chefkoch.de/
https://closetcooking.com/
https://cookeatshare.com/
https://cookieandkate.com/
https://cookpad.com/
https://cookstr.com/
https://copykat.com/
https://countryliving.com/
https://cuisineaz.com/
https://cybercook.com.br/
https://delish.com/
https://domesticate-me.com/
https://downshiftology.com/
https://www.dr.dk/
https://www.eatingbirdfood.com/
https://eatsmarter.de/
https://eatwhattonight.com/
https://recipes.farmhousedelivery.com/
https://fifteenspatulas.com/
https://finedininglovers.com/
https://fitmencook.com/
https://food.com/
https://foodandwine.com/
https://foodnetwork.com/
https://foodrepublic.com/
https://geniuskitchen.com/
https://giallozafferano.it/
https://gimmesomeoven.com/
https://recietas.globo.com/
https://gonnawantseconds.com/
https://gousto.co.uk/
https://halfbakedharvest.com/
https://www.hassanchef.com/
https://www.heb.com/
https://heinzbrasil.com.br/
https://hellofresh.com/
https://hellofresh.co.uk/
https://www.hellofresh.de/
https://hostthetoast.com/
https://101cookbooks.com/
https://receitas.ig.com.br/
https://inspiralized.com/
https://jamieoliver.com/
https://justbento.com/
https://kennymcgovern.com/
https://www.kingarthurbaking.com
https://kochbar.de/
https://kuchnia-domowa.pl/
https://littlespicejar.com/
http://livelytable.com/
https://lovingitvegan.com/
https://lecremedelacrumb.com/
https://marmiton.org/
https://matprat.no/
https://www.melskitchencafe.com/
http://mindmegette.hu/
https://minimalistbaker.com/
https://misya.info/
https://momswithcrockpots.com/
http://motherthyme.com/
https://mybakingaddiction.com/
https://myrecipes.com/
https://healthyeating.nhlbi.nih.gov/
https://nourishedbynutrition.com/
https://nutritionbynathalie.com/blog
https://ohsheglows.com/
https://www.paleorunningmomma.com/
https://www.panelinha.com.br/
https://paninihappy.com/
https://popsugar.com/
https://przepisy.pl/
https://purelypope.com/
https://purplecarrot.com/
https://rachlmansfield.com/
https://realsimple.com/
https://recipietineats.com/
https://seriouseats.com/
https://simplyquinoa.com/
https://simplyrecipes.com/
https://simplywhisked.com/
https://skinnytaste.com/
https://southernliving.com/
https://spendwithpennies.com/
https://www.thespruceeats.com/
https://steamykitchen.com/
https://streetkitchen.hu/
https://sunbasket.com/
https://sweetpeasandsaffron.com/
https://tastesoflizzyt.com
https://tasteofhome.com
https://tastykitchen.com/
https://thekitchn.com/
https://thenutritiouskitchen.co/
https://thepioneerwoman.com/
https://thespruceeats.com/
https://thevintagemixer.com/
https://thewoksoflife.com/
https://tine.no/
https://tudogostoso.com.br/
https://twopeasandtheirpod.com/
https://vanillaandbean.com/
https://vegolosi.it/
https://watchwhatueat.com/
https://whatsgabycooking.com/
https://en.wikibooks.org/
https://yummly.com/

"""

from .acouplecooks import ACoupleCooksScraper
from .allrecipes import AllRecipesScraper
from .amazingribs import AmazingRibsScraper
from .ambitiouskitchen import AmbitiousKitchenScraper
from .bbcfood import BBCFoodScraper
from .bbcgoodfood import BBCGoodFoodScraper
from .bonappetit import BonAppetitScraper
from .claudiaabril import ClaudiaAbrilScraper
from .eatsmarter import EatSmarterScraper
from .epicurious import EpicuriousScraper
from .greatbritishchefs import GreatBritishChefsScraper
from .myrecipes import MyRecipesScraper
from .nytimescooking import NYTimesCookingScraper
from .tasty import TastyScraper
from .thehappyfoodie import TheHappyFoodieScraper

SCRAPER_LIST = [
    ACoupleCooksScraper,
    AllRecipesScraper,
    AmazingRibsScraper,
    AmbitiousKitchenScraper,
    BBCFoodScraper,
    BBCGoodFoodScraper,
    BonAppetitScraper,
    ClaudiaAbrilScraper,
    EatSmarterScraper,
    EpicuriousScraper,
    GreatBritishChefsScraper,
    MyRecipesScraper,
    NYTimesCookingScraper,
    TastyScraper,
    TheHappyFoodieScraper,
]

SCRAPERS = {s.NAME: s for s in SCRAPER_LIST}


def load_all_data():
    """
    Returns a dict() with loaded data for all available scrapers
    """
    return {s.NAME: s().load_from_datafile() for s in SCRAPER_LIST}


def update_all_scrapers():
    """
    Runs scrape_range on every scraper. This will take a while...
    The scrapers with date sitemaps take several minutes just to get all IDs.
    """
    for S in SCRAPER_LIST:
        s = S()
        print("=" * 50)
        print("=" * 10 + f"{s.NAME:^30}" + "=" * 10)
        print("=" * 50)
        s.scrape_range()
