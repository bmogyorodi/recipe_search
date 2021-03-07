import re
import html
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import unidecode
from .models import (Token, RecipeToken, Ingredient, RecipeIngredient, Tag)
from .utils import (parse_ingredients, preprocess_ingredient_string, postprocess_ingredient_string,
                    preprocess_tags)


class Indexer:
    def __init__(self):
        self._token_re = re.compile(r'[a-z\']+(?<!\'s)')
        self._andor_re = re.compile(r' and | or ')
        # Download "stopwords" if not available
        try:
            stopwords.words('english')
        except LookupError:
            import nltk
            nltk.download("stopwords")
        finally:
            self._stopwords = stopwords.words('english')
        # Download "wordnet" if not available
        try:
            WordNetLemmatizer().lemmatize("fail?")
        except LookupError:
            import nltk
            nltk.download("wordnet")
        finally:
            self._wnl = WordNetLemmatizer()

        self.text_part_to_int = {
            "title": 1, "author": 2, "instructions": 3, "ingredients": 4}

    def _preprocess_text(self, text):
        text = html.unescape(text.replace('&amp;', '&'))
        text = unidecode.unidecode(text)  # Replaces â with a, é with e etc.
        return [self._wnl.lemmatize(token.strip("'")) for token in self._token_re.findall(text.lower())
                if token.strip("'") and token.strip("'") not in self._stopwords]

    def index_recipe(self, recipe_obj, recipe):
        pos = 0

        # Categorize different parts of the recipe for indexing
        recipe_text = {
            "title": recipe["title"],
            "ingredients": " ".join(recipe["ingredients"]),
            "instructions": recipe["instructions"],
            "author": recipe["author"] if recipe["author"] is not None else ""
        }

        # Create RecipeIngredients
        recipe_ingredients = []
        for parsed_ing in parse_ingredients(
                map(preprocess_ingredient_string, recipe["ingredients"])):
            # Name must be parsed correctly, otherwise no point
            name = parsed_ing.get("name")
            if name is None:
                continue
            # Try splitting on " and "/" or " for ingredient alternatives
            for name in self._andor_re.split(name):
                name = postprocess_ingredient_string(name)
                ing_obj, _ = Ingredient.objects.get_or_create(title=name)
                recipe_ingredients.append(
                    RecipeIngredient(recipe=recipe_obj, ingredient=ing_obj))
        RecipeIngredient.objects.bulk_create(recipe_ingredients)

        # Create Tags
        for tag_title in preprocess_tags(recipe.get("cuisine")):
            recipe_obj.tags.add(Tag.objects.get_or_create(title=tag_title)[0])

        # Create RecipeTokens
        recipe_token = []
        recipe_length = 0
        for text_part, text in recipe_text.items():
            tokens = self._preprocess_text(text)
            token_type = self.text_part_to_int[text_part]
            for token in tokens:
                pos += 1
                token_obj, _ = Token.objects.get_or_create(title=token)
                recipe_token.append(
                    RecipeToken(token=token_obj,
                                recipe=recipe_obj,
                                position=pos,
                                token_type=token_type))
            recipe_length += len(tokens)
        RecipeToken.objects.bulk_create(recipe_token)
        recipe_obj.length = recipe_length
        recipe_obj.save()
