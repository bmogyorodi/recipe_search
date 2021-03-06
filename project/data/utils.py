import re
import html
import subprocess
import tempfile
import unidecode
from django.conf import settings
from ingredient_phrase_tagger.training import utils


def parse_ingredients(input_text):
    with tempfile.NamedTemporaryFile(mode='w') as input_file:
        input_file.write(utils.export_data(input_text))
        input_file.flush()
        output = subprocess.check_output(
            ['crf_test', '--verbose=1', '--model',
             settings.INGREDIENT_PHRASE_TAGGER_MODEL,
             input_file.name]).decode('utf-8')
        return utils.import_data(output.split("\n"))


def parse_ingredient_quantity(quantity):
    try:
        f = float(quantity)
        return f if f > 0 else None
    except TypeError:  # quantity is None
        return None
    except:
        r = re.compile(r".*(\d+)\s*/\s*(\d+).*")
        m = r.match(quantity)
        if m:
            return float(m.group(1)) / float(m.group(2))
        return None


def parse_nutrient(nutrient):
    if nutrient is None:
        return None
    try:
        f = float(nutrient)
        return f if f > 0 else None
    except:
        r = re.compile(r"(\d*\.\d*)\s*g")  # e.g. "6.7 g" or " .55 g "
        s = r.search(nutrient)
        if s:
            try:
                f = float(s.group(1))
                return f if f > 0 else None
            except:
                return None
        return None


def truncate(string, length):
    return string if len(string) < length else string[:length - 3] + "..."


def parse_html_text(text):
    if text is None:
        return ""
    text = re.sub(r"<!--.*-->", "", text)  # Remove HTML comments
    # Convert HTML entities to Unicode chars
    text = html.unescape(text.replace("&amp;", "&"))
    return text.strip()


def parse_title(title, max_length):
    title = parse_html_text(title)
    if len(title) >= max_length:
        # Attempt to split on ":"
        title = title.split(":")[0].strip()
    return truncate(title, max_length)


def parse_total_time(total_time):
    if isinstance(total_time, int):
        if total_time == 0:
            return None
        else:
            return total_time
    elif isinstance(total_time, str):
        re_str = r"((?P<hours>\d+) hour(s)?)?( )?((?P<minutes>\d+) minute(s)?)?(,)?.*"
        m = re.match(re_str, total_time)
        if m:
            hours = int(m.group('hours')) if m.group('hours') else 0
            minutes = int(m.group('minutes')) if m.group('minutes') else 0
            return hours * 60 + minutes
        else:
            return None
    else:
        return None


pattern_nonalphanum = re.compile('[^\w ]')
pattern_brackets = re.compile('\([^)(]*\)|\{[^}{]*\}|\[[^][]*\]')
pattern_unicode_fractions = re.compile(
    "\u00BC|\u00BD|\u00BE|\u2150|\u2151|\u2152|\u2153|\u2154|\u2155|\u2156|"
    "\u2157|\u2158|\u2159|\u215A|\u215B|\u215C|\u215D|\u215E|\u215F")
# Mixed fraction, qty range, and alternates handling
mixed_fraction = r"\d*\s*\d+\/\d+"           # e.g. "5 1/4" OR "51/4"
unit = r"[a-z]+"                             # simple string unit
qty = f"({mixed_fraction}|\d+)"              # mixed fraction or just a number
qty_or_range = f"({qty}\s*-\s*{qty}|{qty})"  # also handle "5 1/4 - 7"
qty_unit = f"{qty_or_range}\s*{unit}"        # including a string unit
alternate_or_single_amount = re.compile(     # e.g. "20-50 ml/4-10 1/8 tsp"
    f"({qty_unit}\s*\/\s*{qty_unit}|{qty_unit})")


def preprocess_ingredient_string(ingredient):
    # Case-fold and remove unicode characters
    ingredient = pattern_unicode_fractions.sub('', ingredient)
    ingredient = unidecode.unidecode(ingredient)
    ingredient = ingredient.lower()
    # Remove parentheses with contents, e.g. (8-oz) steak
    ingredient = pattern_brackets.sub('', ingredient)
    # Essentially remove any possible unit, incl. ranges, mixed fractions, etc.
    # ingredient = alternate_or_single_amount.sub('', ingredient)
    # Remove non-alphanumerical characters, e.g. unclosed parentheses
    ingredient = pattern_nonalphanum.sub('', ingredient)
    # Replace common shorthands with full words
    ingredient = ingredient.replace('tsp', 'teaspoons')
    ingredient = ingredient.replace('tbsp', 'tablespoons')
    ingredient = ingredient.replace('oz', 'ounces')
    ingredient = ingredient.replace('kg', 'g')  # matches better but wrong
    # Unnecessary whitespace is dealt with in parse_ingredients
    return ingredient


pattern_ml = re.compile('^((\d)+ ?)?ml')  # e.g. "140 ml" OR "140ml" or "ml"
# e.g. 34cups OR 34 cups OR 1 cup
pattern_cups = re.compile('^(\d+)? ?cup(s)?')
pattern_numqty = re.compile('^\d+( )?')  # numbers at start of string


def postprocess_ingredient_string(ingredient):
    # Since string beginning is important, strip before doing anything else
    ingredient = ingredient.strip()
    if 'ounces' in ingredient:
        # e.g. "100 milliliters10fl ounces double cream"
        ingredient = ingredient.split('ounces')[1]
    if 'lb' in ingredient:
        # e.g. "450 grams1lb caster sugar"
        ingredient = ingredient.split('lb')[1]
    if ingredient[:2] == 'g ':
        ingredient = ingredient[2:]  # e.g. "g caster sugar"
    if ingredient[:2] == 'x ':
        ingredient = ingredient[2:]  # e.g. "x tomatoes"
    ingredient = pattern_ml.sub('', ingredient)  # e.g. 140ml milk
    ingredient = pattern_cups.sub('', ingredient)  # e.g. 34 cups flour
    ingredient = pattern_numqty.sub('', ingredient)  # e.g. 30 carrots
    ingredient = ingredient.strip()
    return ingredient


tag_separator = re.compile(r",|\/")
tag_remove = re.compile(r"inspired|styled?|n\/a|https?[^\s]+")


def preprocess_tags(tags):
    if tags is None:
        return []
    # Case-fold and remove parentheses, e.g. "vegan (plant based)" -> "vegan "
    tags = pattern_brackets.sub("", tags.lower())
    # Replace "-" with spaces, e.g. "spanish-inspired" -> "spanish inspired"
    tags = tags.replace("-", " ")
    # Remove redundant words like "inspired", or empty tag "n/a"
    tags = tag_remove.sub("", tags)
    # Split on ',' and '/' and strip whitespace
    tags = map(str.strip, tag_separator.split(tags))
    # Filter out empty strings, potentially cause by removing some tags
    return [t for t in tags if t != ""]
