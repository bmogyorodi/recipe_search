import re
import html


class DataLoader():
    HTML_COMMENT_RE = re.compile(r"<!--.*-->")
    TOTAL_TIME_RE = re.compile(r"((?P<hours>\d+) hour(s)?)?( )?((?P<minutes>\d+) minute(s)?)?(,)?.*")

    @classmethod
    def parse_title(title):
        title = DataLoader.HTML_COMMENT_RE.sub('', title)  # Remove HTML comments
        title = html.unescape(title.replace('&amp;', '&'))  # Convert HTML entities to Unicode chars
        return title

    @classmethod
    def parse_total_time(total_time):
        if isinstance(total_time, int):
            return total_time
        elif isinstance(total_time, str):
            m = DataLoader.TOTAL_TIME_RE.match(total_time)
            if m:
                hours = int(m.group('hours')) if m.group('hours') else 0
                minutes = int(m.group('minutes')) if m.group('minutes') else 0
                return hours * 60 + minutes
            else:
                return None
        else:
            return None
