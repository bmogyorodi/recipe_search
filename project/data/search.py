from .indexer import Indexer
from .spelling import SpellChecker
from .models import RecipeToken, Recipe
from django.db.models import Count
from collections import defaultdict
from math import log10


class RankedSearch:
    def __init__(self):
        self.indexer = Indexer()
        self.doc_count = Recipe.objects.count()
        self.spell_checker = SpellChecker()

    def search(self, query):
        tokens = self.indexer._preprocess_text(query)

        # Correct the spelling of the tokens
        tokens = self.spell_checker.correct_spelling(tokens)

        scores = defaultdict(float)
        for token in tokens:
            # Find the document frequency (df) from the inverted index
            df = RecipeToken.objects.filter(token__title=token).count()

            # Calculate the term frequency (tf) for each document
            tfs = (RecipeToken.objects.filter(token__title=token)
                                      .values("recipe")
                                      .annotate(tf=Count("token"))
                                      .values_list("recipe", "tf"))

            for recipe_id, tf in tfs:
                scores[recipe_id] += (1 + log10(tf)) * log10(self.doc_count / df)
        return sorted(scores.items(), key=lambda item: item[1], reverse=True)
