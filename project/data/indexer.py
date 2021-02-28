import re
import html
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from .models import (Token, RecipeToken, Ingredient, RecipeIngredient, Tag)
from .utils import (parse_ingredients, preprocess_ingredient_string,
                    parse_ingredient_quantity)


class Indexer:
    def __init__(self):
        self._token_re = re.compile(r'[a-z\']+')
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
            name = parsed_ing.get("name")
            # Name must be parsed correctly, otherwise no point
            if name is None:
                continue
            ing_obj, _ = Ingredient.objects.get_or_create(title=name)
            quantity = parse_ingredient_quantity(parsed_ing.get("qty"))
            recipe_ingredients.append(
                RecipeIngredient(recipe=recipe_obj,
                                 ingredient=ing_obj,
                                 quantity=quantity,
                                 unit=parsed_ing.get("unit") or ""))
        RecipeIngredient.objects.bulk_create(recipe_ingredients)

        # Create Tags
        for tag_title in map(
                str.strip, recipe.get("cuisine", "").lower().split(",")):
            # Don't want the empty string
            if tag_title == "":
                continue
            recipe_obj.tags.add(Tag.objects.get_or_create(title=tag_title)[0])

        # Create RecipeTokens
        recipe_token = []
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
        RecipeToken.objects.bulk_create(recipe_token)
