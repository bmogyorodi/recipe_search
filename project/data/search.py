from .indexer import Indexer
from .models import RecipeToken, Recipe
from django.db.models import Count
from collections import defaultdict
from math import log10


class RankedSearch:
    def __init__(self):
        self.indexer = Indexer()
        self.doc_count = Recipe.objects.count()

    def search(self, query):
        tokens = self.indexer._preprocess_text(query)
        scores = defaultdict(float)
        for token in tokens:
            # Find the document frequency (df) from the inverted index
            df = RecipeToken.objects.filter(token__title=token).count()

            # Calculate the term frequency (tf) for each document
            tfs = dict(RecipeToken.objects.filter(token__title=token)
                                          .values("recipe")
                                          .annotate(tf=Count("token"))
                                          .values_list("recipe", "tf"))

            for recipe_id, tf in tfs.items():
                weight = (1 + log10(tf)) * log10(self.doc_count / df)
                scores[recipe_id] += weight
        return sorted(scores.items(), key=lambda item: item[1], reverse=True)
