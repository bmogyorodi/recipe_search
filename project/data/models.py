from django.db import models

from core.models import CleanableModel
from .data_loader import DataLoader
from .utils import (parse_ingredient_quantity, parse_nutrient, truncate)


class Token(CleanableModel):
    """
    Tokens appearing within the Index
    """
    title = models.CharField(max_length=127)
    recipes = models.ManyToManyField(
        "Recipe",
        through="RecipeToken",
        through_fields=("token", "recipe"),
        related_name="tokens",
        related_query_name="token")

    def clean(self, *args, **kwargs):
        # Get rid of whitespace, lower-case, and truncate
        self.title = truncate(self.title.strip().lower(), 127)
        self.is_cleaned = True


class RecipeToken(models.Model):
    class TokenType(models.IntegerChoices):
        TITLE = 1
        AUTHOR = 2
        INSTRUCTIONS = 3
        INGREDIENTS = 4

    token = models.ForeignKey("Token", on_delete=models.CASCADE)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    token_type = models.IntegerField(choices=TokenType.choices)


class Tag(CleanableModel):
    title = models.CharField(max_length=64)

    def clean(self, *args, **kwargs):
        # Get rid of whitespace, lower-case, and truncate
        self.title = truncate(self.title.strip().lower(), 64)
        self.is_cleaned = True

    def __str__(self):
        return self.title


class Ingredient(CleanableModel):
    title = models.CharField(max_length=127)

    def clean(self, *args, **kwargs):
        # Get rid of whitespace, lower-case, and truncate
        self.title = truncate(self.title.strip().lower(), 127)
        self.is_cleaned = True

    def __str__(self):
        return self.title


class RecipeIngredient(CleanableModel):
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    ingredient = models.ForeignKey("Ingredient", on_delete=models.CASCADE)
    quantity = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=64, blank=True)

    def clean(self, *args, **kwargs):
        self.unit = truncate(self.unit, 64)
        self.quantity = parse_ingredient_quantity(self.quantity)
        self.is_cleaned = True


class Recipe(CleanableModel):
    """
    Model containing displayed information about a recipe as well as metadata.
    The tuple (source, source_id) uniquely corresponds to original raw source.
    """

    RATINGS_MAX = 5.0
    RATINGS_MIN = 0.0

    # ID is implicit and corresponds to the unique identifier for a recipe
    # At least one recipe has title length 746
    title = models.CharField(max_length=127)
    # At least one canonical url has 203 characters from our current dataset
    canonical_url = models.TextField(blank=True)
    # At least one image url has 251 characters from our current dataset
    image = models.TextField(blank=True)
    author = models.CharField(max_length=127, blank=True)

    # e.g. "ambitiouskitchen"
    source = models.CharField(max_length=50)
    # Maximum length is 169 so far so hopefully shouldn't cause problems
    source_id = models.CharField(max_length=255)

    ingredients = models.ManyToManyField(
        "Ingredient", through="RecipeIngredient",
        related_name="recipes",
        related_query_name="recipe")

    # Float in range [0, 5] or None
    ratings = models.FloatField(blank=True, null=True)
    # The text total time converted to an integer in minutes
    total_time = models.PositiveIntegerField(blank=True, null=True)
    # This can vary from "6 serving(s) to "3 dozen kolacky", so string
    yields = models.CharField(max_length=64, blank=True)

    # TODO: split cuisines on ",", strip, lowercase, create models
    tags = models.ManyToManyField(
        "Tag",
        related_name="recipes",
        related_query_name="recipe")

    # Nutrients kept in original camel-case name format
    # 'value' is not used very often and doesn't contain anything useful
    servingSize = models.CharField(max_length=64, blank=True)
    calories = models.FloatField(blank=True, null=True)
    carbohydrateContent = models.FloatField(blank=True, null=True)
    cholesterolContent = models.FloatField(blank=True, null=True)
    fatContent = models.FloatField(blank=True, null=True)
    fiberContent = models.FloatField(blank=True, null=True)
    proteinContent = models.FloatField(blank=True, null=True)
    saturatedFatContent = models.FloatField(blank=True, null=True)
    sodiumContent = models.FloatField(blank=True, null=True)
    sugarContent = models.FloatField(blank=True, null=True)
    transFatContent = models.FloatField(blank=True, null=True)
    unsaturatedFatContent = models.FloatField(blank=True, null=True)

    def clean(self, *args, **kwargs):
        # Rating must be in range [0, 5] otherwise set null
        if self.ratings > self.RATINGS_MAX or self.ratings < self.RATINGS_MIN:
            self.ratings = None
        # Truncate and escape title and author to their max length
        self.title = truncate(DataLoader.parse_title(self.title), 127)
        self.author = truncate(DataLoader.parse_title(self.author), 127)
        # Convert total_time to an integer if not already parsed
        self.total_time = DataLoader.parse_total_time(self.total_time)
        # Serving size and yields could also potentially overflow max length
        self.servingSize = truncate(self.servingSize, 64)
        self.yields = truncate(self.yields, 64)
        # Parse nutrients
        self.calories = parse_nutrient(self.calories)
        self.carbohydrateContent = parse_nutrient(self.carbohydrateContent)
        self.cholesterolContent = parse_nutrient(self.cholesterolContent)
        self.fatContent = parse_nutrient(self.fatContent)
        self.fiberContent = parse_nutrient(self.fiberContent)
        self.proteinContent = parse_nutrient(self.proteinContent)
        self.saturatedFatContent = parse_nutrient(self.saturatedFatContent)
        self.sodiumContent = parse_nutrient(self.sodiumContent)
        self.sugarContent = parse_nutrient(self.sugarContent)
        self.transFatContent = parse_nutrient(self.transFatContent)
        self.unsaturatedFatContent = parse_nutrient(self.unsaturatedFatContent)
        # The model is cleaned now, but many-to-many still needs cleaning
        self.is_cleaned = True

    def __str__(self):
        return self.title
