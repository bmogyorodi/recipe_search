import re
import html
import subprocess
import tempfile
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
