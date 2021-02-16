import re
import html


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
    text = html.unescape(text.replace("&amp;", "&"))  # Convert HTML entities to Unicode chars
    return text.strip()


def parse_title(title, max_length):
    title = parse_html_text(title)
    if len(title) >= max_length:
        # Attempt to split on ":"
        title = title.split(":")[0].strip()
    return truncate(title, max_length)


def parse_total_time(total_time):
    if isinstance(total_time, int):
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
