from .indexer import Indexer
from .spelling import SpellChecker
from .models import RecipeToken, Recipe
from collections import defaultdict, Counter
from django.db.models import Count, Min
from math import log10
import numpy as np


class RankedSearch:
    def __init__(self):
        self.indexer = Indexer()
        self.doc_count = Recipe.objects.count()
        self.spell_checker = SpellChecker()

    def search(self, query):
        def tfidf_weight(tf, df, N):
            return (1 + log10(tf)) * log10(N / df)

        def bm25_weight(tf, df, N, k=1.5):
            # TODO
            return

        tokens = self.indexer._preprocess_text(query)

        # Correct the spelling of the tokens
        tokens = self.spell_checker.correct_spelling(tokens)

        scores = defaultdict(float)

        for token in tokens:
            recipetoken_objs = RecipeToken.objects.filter(token__title=token)

            # Find the document frequency (df) from the inverted index
            df = recipetoken_objs.count()

            # Calculate the term frequency (tf) for each document
            tfs = (recipetoken_objs.values("recipe_id")
                                   .annotate(min_token_type=Min("token_type"), tf=Count("*"))
                                   .values_list("recipe_id", "min_token_type", "tf"))

            # Update recipe tfidf vectors
            for recipe_id, min_token_type, tf in tfs:
                scores[recipe_id] += tfidf_weight(tf, df, self.doc_count) * \
                    (2 if min_token_type == 1 else 1)

        return sorted(scores.items(), key=lambda item: item[1], reverse=True)

    """
    def search(self, query):
        def tfidf_weight(tf, df, N):
            return (1 + log10(tf)) * log10(N / df)

        def cosine_similarity(v1, v2):
            return v1.dot(v2) / (np.sqrt(v1.dot(v1)) * np.sqrt(v2.dot(v2)))

        tokens = self.indexer._preprocess_text(query)

        # Correct the spelling of the tokens
        tokens = self.spell_checker.correct_spelling(tokens)

        query_token_counts = list(Counter(tokens).items())
        tfidf_vectors = defaultdict(lambda: np.zeros(len(query_token_counts)))
        query_tfidf_vector = np.zeros(len(query_token_counts))
        scores = defaultdict(float)

        for i in range(len(query_token_counts)):
            token, query_tf = query_token_counts[i]

            # Find the document frequency (df) from the inverted index
            df = RecipeToken.objects.filter(token__title=token).count()

            # Calculate the term frequency (tf) for each document
            tfs = Counter(RecipeToken.objects.filter(token__title=token)
                                             .values_list("recipe__id", flat=True))

            # Update query tfidf vector
            query_tfidf_vector[i] = tfidf_weight(query_tf, df, self.doc_count)

            # Update recipe tfidf vectors
            for recipe_id, tf in tfs.items():
                tfidf_vectors[recipe_id][i] = tfidf_weight(tf, df, self.doc_count)

        for recipe_id, tfidf_vector in tfidf_vectors.items():
            scores[recipe_id] = cosine_similarity(query_tfidf_vector, tfidf_vector)

        return sorted(scores.items(), key=lambda item: item[1], reverse=True)
    """
