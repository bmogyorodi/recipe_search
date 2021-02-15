from django.db import models


class Token(models.Model):
    title = models.CharField(max_length=127)
    recipes = models.ManyToManyField(
        "Recipe",
        through="RecipeToken",
        through_fields=("token", "recipe"),
        related_name="tokens",
        related_query_name="token")


class RecipeToken(models.Model):
    token = models.ForeignKey("Token", on_delete=models.CASCADE)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    # TODO: Django choice field with int
    # TODO: title, instructions, ingredient, author
    token_type = models.IntegerChoices  # ...


class Tag(models.Model):
    title = models.CharField(max_length=50)


class Ingredient(models.Model):
    title = models.CharField(max_length=128)
    # TODO References to recipes with ingredient

    def __str__(self):
        return str(self.title)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    ingredient = models.ForeignKey("Ingredient", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    unit = models.CharField(max_length=128, blank=True)


class Recipe(models.Model):
    """
    Model containing displayed information about a recipe

    # TODO some are stupidly long strings, up to 110 characters
    # e.g. '12 hours, 2 hours preparation time, 10 hours inactive'
    total_time

    # TODO: max length is 307, so likely also long strings
    # TODO: @Dimitris parse into a number
    yields

    # TODO: @Peter store nutrition, each nutrient in a separate field with NB
    """

    # ID is implicit and corresponds to the
    # TODO: at least one recipe has title length 746
    title = models.CharField(max_length=128)
    # At least one canonical url has 203 characters from our current dataset
    canonical_url = models.TextField(blank=True)
    # At least one image url has 251 characters from our current dataset
    image = models.TextField(blank=True)
    author = models.CharField(max_length=127, blank=True)

    # Index UID, because default id doesn't reset after emptying DB
    uid = models.PositiveIntegerField(unique=True)
    # e.g. "ambitiouskitchen"
    source = models.CharField(max_length=50)
    # Maximum length is 169 so far so hopefully shouldn't cause problems
    source_id = models.CharField(max_length=255)

    # TODO: @Peter need to ensure rating is in range [0, 5] otherwise set null
    ratings = models.FloatField(blank=True, null=True)
    # TODO: Clean up and concatenate in a readable + parseable format
    ingredients = models.TextField(blank=True)

    # TODO: split cuisines on ",", strip, lowercase, create models
    tags = models.ManyToManyField(
        Tag,
        related_name="recipes",
        related_query_name="recipe")

    # TODO: need to clean and truncate title, author, and possibly others
    # __init__ isn't enough, clean() should be the way to go

    def __str__(self):
        return self.title
