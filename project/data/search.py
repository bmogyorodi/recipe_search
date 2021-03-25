from .indexer import Indexer
from .spelling import SpellChecker
from .models import RecipeToken, Recipe, RecipeIngredient, RecipeTokenFrequency, Token
from collections import defaultdict
import random
from django.db.models import Count, Min, Avg
from math import log10
import logging
import time

logger = logging.getLogger(__name__)


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

    def search(self, query):
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
            df = recipetoken_objs.aggregate(Count("recipe_id", distinct=True))["recipe_id__count"]

            # Calculate the term frequency (tf) for each document
            tfs = (recipetoken_objs.values("recipe_id", "recipe__length")
                                   .annotate(min_token_type=Min("token_type"), tf=Count("*"))
                                   .values_list("recipe_id", "min_token_type", "tf", "recipe__length"))

            # Update recipe tfidf vectors
            for recipe_id, min_token_type, tf, length in tfs:
                scores[recipe_id] += bm25_weight(tf, df, length) * \
                    (5 if min_token_type == 1 else 1)
        return [x[0] for x in sorted(scores.items(), key=lambda item: item[1], reverse=True)]

    def new_search(self, query):
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
            # Find the document frequency (df) from the inverted index
            df = Token.objects.get(title=token).recipe_count

            tfs = (RecipeTokenFrequency.objects
                                       .filter(token__title=token)
                                       .values_list("recipe", "in_title", "tf", "recipe__length"))

            # Update recipe tfidf vectors
            for recipe_id, in_title, tf, length in tfs:
                scores[recipe_id] += bm25_weight(tf, df, length) * \
                    (5 if in_title else 1)
        return [x[0] for x in sorted(scores.items(), key=lambda item: item[1], reverse=True)]

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
