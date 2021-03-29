from .indexer import Indexer
from .spelling import SpellChecker
from .models import RecipeToken, Recipe, RecipeIngredient, RecipeTokenFrequency, Token
from collections import defaultdict
import random
from django.db.models import Count, Min, Avg
from math import log10
import numpy as np
import pandas as pd
import time


def recipe_search(query="", include=[], must_have=[], exclude=[], count=100):
    if len(include) == 0 and len(must_have) == 0 and len(exclude) == 0:
        recipe_ids = None
    else:
        recipe_ids = BooleanIngredientSearch().search(include=include,
                                                      must_have=must_have,
                                                      exclude=exclude)

    if len(query) == 0:
        random.seed(10)
        res = list(recipe_ids) if recipe_ids is not None else []
        random.shuffle(res)
    else:
        res = RankedSearch().search(query)

    if recipe_ids is not None:
        res = [recipe_id for recipe_id in res if recipe_id in recipe_ids]

    return [Recipe.objects.get(id=recipe_id) for recipe_id in res[:count]]


class BooleanIngredientSearch:
    def _get_recipes_with_ingr(self, ingr):
        """
        Finds all recipes with an ingredient which has the given ingredient as substring
        """
        return set(RecipeIngredient.objects.filter(
            ingredient__title__contains=ingr).values_list("recipe", flat=True))

    def search(self, include=[], must_have=[], exclude=[]):
        res = set()
        if len(include) == 0:
            res = set(Recipe.objects.all().values_list("id", flat=True))

        first_include = True

        for ingredient in include + must_have:
            recipes_with_ingr = self._get_recipes_with_ingr(ingredient.lower())
            if ingredient in must_have:
                if first_include:
                    first_include = False
                    res = recipes_with_ingr
                else:
                    res &= recipes_with_ingr
            else:
                res |= recipes_with_ingr

        for ingredient in exclude:
            recipes_with_ingr = self._get_recipes_with_ingr(ingredient.lower())
            res -= recipes_with_ingr

        return res


class RankedSearch:
    AVG_LENGTH = Recipe.objects.aggregate(Avg("length"))["length__avg"]
    DOC_COUNT = Recipe.objects.count()

    def __init__(self):
        self.indexer = Indexer()
        self.spell_checker = SpellChecker()

    def old_search(self, query):
        def tfidf_weight(tf, df):
            return (1 + log10(tf)) * log10(self.DOC_COUNT / df)

        def bm25_weight(tf, df, L, k=1.5):
            tf_component = tf / (k * L / self.AVG_LENGTH + tf + 0.5)
            idf_component = log10((self.DOC_COUNT - df + 0.5) / (df + 0.5))
            return tf_component * idf_component

        tokens = self.indexer._preprocess_text(query)

        # Correct the spelling of the tokens
        tokens = self.spell_checker.correct_spelling(tokens)

        scores = defaultdict(float)

        for token in tokens:
            recipetoken_objs = RecipeToken.objects.filter(token__title=token)

            # Find the document frequency (df) from the inverted index
            df = recipetoken_objs.aggregate(Count("recipe_id", distinct=True))[
                "recipe_id__count"]

            # Calculate the term frequency (tf) for each document
            tfs = (recipetoken_objs.values("recipe_id", "recipe__length")
                                   .annotate(min_token_type=Min("token_type"), tf=Count("*"))
                                   .values_list("recipe_id", "min_token_type", "tf", "recipe__length"))

            # Update recipe tfidf vectors
            for recipe_id, min_token_type, tf, length in tfs:
                scores[recipe_id] += bm25_weight(tf, df, length) * \
                    (5 if min_token_type == 1 else 1)
        return [x[0] for x in sorted(scores.items(), key=lambda item: item[1], reverse=True)]

    def search(self, query):
        def tfidf_weight(tf, df):
            return (1 + log10(tf)) * log10(self.DOC_COUNT / df)

        def bm25_weight(tf, df, L, k=1.5):
            tf_component = tf / (k * L / self.AVG_LENGTH + tf + 0.5)
            idf_component = log10((self.DOC_COUNT - df + 0.5) / (df + 0.5))
            return tf_component * idf_component

        def bm25_weights_vector(tfs, df, lengths, k=1.5):
            tf_components = tfs / (k * lengths / self.AVG_LENGTH + tfs + 0.5)
            idf_component = np.log10((self.DOC_COUNT - df + 0.5) / (df + 0.5))
            return tf_components * idf_component

        tokens = self.indexer._preprocess_text(query)

        # Correct the spelling of the tokens
        tokens = self.spell_checker.correct_spelling(tokens)

        scores = defaultdict(float)

        for token in tokens:
            # Find the document frequency (df) from the inverted index
            # start_time = time.time()
            df = Token.objects.get(title=token).recipe_count
            # print(time.time() - start_time)

            # start_time = time.time()
            res = (RecipeTokenFrequency.objects.filter(token__title=token)
                                               .values("recipe", "in_title", "tf", "recipe_length"))
            # print(time.time() - start_time)

            # start_time = time.time()
            res = pd.DataFrame.from_records(res)
            recipe_ids = res["recipe"]
            in_titles = res["in_title"]
            tfs = res["tf"]
            lengths = res["recipe_length"]
            # print(time.time() - start_time)

            # start_time = time.time()
            weights = bm25_weights_vector(
                tfs, df, lengths) * (in_titles * 4 + 1)
            # print(time.time() - start_time)

            # start_time = time.time()
            for i in range(len(recipe_ids)):
                scores[recipe_ids[i]] += weights[i]
            # print(time.time() - start_time)

        return [x[0] for x in sorted(scores.items(), key=lambda item: item[1], reverse=True)]
