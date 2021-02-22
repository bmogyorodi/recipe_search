import re
import html
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from .models import Token, RecipeToken


class Indexer:
    def __init__(self):
        self._stopwords = stopwords.words('english')
        self._token_re = re.compile(r'[a-z\']+')
        self._wnl = WordNetLemmatizer()
        self.text_part_to_int = {"title": 1, "author": 2, "instructions": 3, "ingredients": 4}

    def _preprocess_text(self, text):
        text = html.unescape(text.replace('&amp;', '&'))
        return [self._wnl.lemmatize(token.strip("'")) for token in self._token_re.findall(text.lower())
                if token.strip("'") and token.strip("'") not in self._stopwords]

    def index_recipe(self, recipe_obj, recipe_text):
        pos = 0
        for text_part, text in recipe_text.items():
            tokens = self._preprocess_text(text)
            token_type = self.text_part_to_int[text_part]
            for token in tokens:
                pos += 1
                token_obj, created = Token.objects.get_or_create(title=token)
                RecipeToken.objects.create(token=token_obj,
                                           recipe=recipe_obj,
                                           position=pos,
                                           token_type=token_type)
