from django.db.models import Count, Max
from .models import Token
import string


def is_known(token):
    return Token.objects.filter(title=token).exists()


def get_token_objects_for_known_tokens(tokens):
    return Token.objects.filter(title__in=tokens)


def find_most_common_correct_token_spelling(token):
    candidates = get_candidates(token)
    if candidates:
        candidate_counts = candidates.annotate(token_count=Count("recipes"))
        max_count = candidate_counts.aggregate(maxcount=Max("token_count"))["maxcount"]
        most_common_token = candidate_counts.filter(token_count=max_count)
        return most_common_token[0].title
    else:
        return None


def get_candidates(token):
    tokens_within_2_edits = tokens_1_edit_away(token) | tokens_2_edits_away(token)
    return get_token_objects_for_known_tokens(tokens_within_2_edits)


def correct_spelling(tokens):
    res = []
    for i in range(len(tokens)):
        token = tokens[i]
        if is_known(token):
            res.append(token)
        else:
            correct_token = find_most_common_correct_token_spelling(token)
            if correct_token is not None:
                res.append(correct_token)
    return res


def tokens_2_edits_away(token):
    res = set()
    for e1 in tokens_1_edit_away(token):
        res |= tokens_1_edit_away(e1)
    return res


def tokens_1_edit_away(token):
    chars = string.ascii_lowercase + "'"
    splits = [(token[:i], token[i:]) for i in range(len(token) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in chars]
    inserts = [L + c + R for L, R in splits for c in chars]
    return set(deletes + transposes + replaces + inserts)
