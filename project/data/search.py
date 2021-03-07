from .indexer import Indexer
from .spelling import SpellChecker
from .models import RecipeToken, Recipe
from django.db.models import Count
from collections import defaultdict, Counter
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
            tfs = (RecipeToken.objects.filter(token__title=token)
                                      .values("recipe")
                                      .annotate(tf=Count("token"))
                                      .values_list("recipe", "tf"))

            # Update query tfidf vector
            query_tfidf_vector[i] = tfidf_weight(query_tf, df, self.doc_count)

            for recipe_id, tf in tfs:
                tfidf_vectors[recipe_id][i] = tfidf_weight(tf, df, self.doc_count)

        for recipe_id, tfidf_vector in tfidf_vectors.items():
            scores[recipe_id] = cosine_similarity(query_tfidf_vector, tfidf_vector)

        return sorted(scores.items(), key=lambda item: item[1], reverse=True)
