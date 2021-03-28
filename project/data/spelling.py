from pathlib import Path
import string
import pickle


class SpellChecker:
    _DATA_DIR = Path(__file__).parent.resolve() / "spellchecker_data"
    _TOKEN_COUNTS_FILENAME = "token_counts.pickle"
    _DATAFILE = _DATA_DIR / _TOKEN_COUNTS_FILENAME

    def __init__(self):
        # Possible the pickle file doesn't exist yet
        if not self._DATAFILE.exists():
            from .data_loader import DataLoader
            DataLoader().construct_spellchecker_data()
        with open(self._DATAFILE, "rb") as f:
            self.token_counts = pickle.load(f)

    def _is_known(self, token):
        """
        Checks whether the given token exists within the database
        """
        return token in self.token_counts

    def _find_most_common_correct_token_spelling(self, token):
        """
        Finds the most common token that is at most 2 edit distances away from the givent token
        """
        candidates = self._get_candidates(token)
        if candidates:
            most_common_token = None
            max_count = 0
            for candidate in candidates:
                candidate_count = self.token_counts[candidate]
                if candidate_count > max_count:
                    most_common_token = candidate
                    max_count = candidate_count
            return most_common_token
        else:
            return None

    def _get_candidates(self, token):
        """
        Finds all tokens within at most two edit distances that exist in the database
        """
        tokens_within_2_edits = self._tokens_1_edit_away(token) | self._tokens_2_edits_away(token)
        return tokens_within_2_edits & self.token_counts.keys()

    def _tokens_2_edits_away(self, token):
        """
        Finds all tokens that are exactly two edit distances away
        """
        res = set()
        for e1 in self._tokens_1_edit_away(token):
            res |= self._tokens_1_edit_away(e1)
        return res

    def _tokens_1_edit_away(self, token):
        """
        Finds all tokens that are exactly one edit distance away
        """
        chars = string.ascii_lowercase + "'"
        splits = [(token[:i], token[i:]) for i in range(len(token) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in chars]
        inserts = [L + c + R for L, R in splits for c in chars]
        return set(deletes + transposes + replaces + inserts)

    def correct_spelling(self, tokens):
        """
        Corrects the spelling of each of the tokens. If the spelling is correct the token is left
        unchanged. If a correct spelling cannot be found, the token is discarded
        """
        res = []
        for i in range(len(tokens)):
            token = tokens[i]
            if self._is_known(token):
                res.append(token)
            else:
                correct_token = self._find_most_common_correct_token_spelling(token)
                if correct_token is not None:
                    res.append(correct_token)
        return res
