import re


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
