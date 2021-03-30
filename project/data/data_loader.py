from .indexer import Indexer
from pathlib import Path
import pickle
import bz2
import os
import time
from datetime import timedelta
from django.db.models import Min, Count

from .spelling import SpellChecker
from .models import Recipe, Source, RecipeToken, RecipeTokenFrequency, Token


class DataLoader():
    _RAW_DATA_DIR = Path(__file__).parent.resolve() / "data"
    SOURCE_INFO_FILENAME = "sources.psv"

    def __init__(self, files_to_load=None):
        self.indexer = Indexer()
        self.filenames = [fn for fn in os.listdir(
            self._RAW_DATA_DIR) if fn.split(".")[-1] == "pbz2"]
        if files_to_load is not None:
            self.filenames = [
                fn for fn in self.filenames if fn in files_to_load]

    def import_datasets(self):
        for filename in self.filenames:
            try:
                self._import_dataset(filename)
            except KeyboardInterrupt:
                print("\nStopping...")
                return

    def _import_dataset(self, filename):
        # Make sure Source information has been loaded
        if Source.objects.count() == 0:
            self.import_source_information()
        # If source doesn't exist, correctly crashes
        source = Source.objects.get(source_id=filename.split(".")[0])
        recipes = self._load_datafile(filename)["recipes"]
        start_time = time.time()

        already_indexed = set(Recipe.objects.filter(
            source=source).values_list("source_raw_id", flat=True))
        total_to_index = len(recipes) - len(already_indexed)

        print("------------------------------------")
        print(f"Indexing {source}")
        print("------------------------------------")
        print(f"Recipes already indexed: {len(already_indexed)}")
        print(f"New recipes to index:    {total_to_index}\n")

        count = 0
        for source_id in recipes.keys() - already_indexed:
            # If recipe is not already in the database, add it
            recipe = recipes[source_id]
            if (
                len(recipe["ingredients"]) > 0 and
                len(recipe["instructions"]) > 0
            ):
                # Remove empty "value" attribute in nutrients if it exists
                nutrients = recipe.get("nutrients", {})
                if "value" in nutrients:
                    del nutrients["value"]

                recipe_obj = Recipe(title=recipe["title"],
                                    canonical_url=recipe["canonical_url"],
                                    image=recipe["image"] if recipe["image"] is not None else "",
                                    author=recipe["author"],
                                    source=source,
                                    source_raw_id=source_id,
                                    ratings=recipe.get("ratings", -1),
                                    total_time=recipe.get("total_time", 0),
                                    yields=recipe.get("yields", ""),
                                    **nutrients)
                recipe_obj.save()

                self.indexer.index_recipe(recipe_obj, recipe)

                count += 1
                total_time = time.time() - start_time
                remaining = total_to_index - count
                average = total_time / count
                total = timedelta(seconds=round(total_time))
                estimated = timedelta(
                    seconds=round(remaining * average))
                print(f" Imported {count} |"
                      f" Remaining {remaining} |"
                      f" Total: {total} |"
                      f" Average/recipe: {average:.2f}s |"
                      f" Estimated: {estimated} |"
                      f" Current ID: {source_id}", "\033[K", end="\r", flush=True)
        print("\n\n")

    def _load_datafile(self, filename):
        with bz2.BZ2File(self._RAW_DATA_DIR / filename, "rb") as f:
            return pickle.load(f)

    def import_source_information(self):
        with open(self._RAW_DATA_DIR / self.SOURCE_INFO_FILENAME, "r") as f:
            f.readline()  # Skip header row
            count = 0
            for line in f:
                count += 1
                source_id, source_name, source_url, favicon_url = line.split(
                    "|")
                Source.objects.get_or_create(
                    source_id=source_id, title=source_name, url=source_url, favicon=favicon_url)
        print(f"Imported information about {count} sources")

    def construct_recipetoken_frequency_table(self):
        RecipeTokenFrequency.objects.all().delete()
        res = (RecipeToken.objects
                          .values("recipe", "token")
                          .annotate(min_token_type=Min("token_type"), tf=Count("*")))

        objs = []
        count = 0
        start_time = time.time()
        for r in res.iterator():
            count += 1
            objs.append(RecipeTokenFrequency(
                token=Token.objects.get(id=r["token"]),
                recipe=Recipe.objects.get(id=r["recipe"]),
                in_title=r["min_token_type"] == 1,
                tf=r["tf"]
            ))
            if len(objs) >= 10000:
                RecipeTokenFrequency.objects.bulk_create(objs)
                objs = []

                print(f"Token {r['token']} "
                      f"| Recipe {r['recipe']} "
                      f"| {count} completed | {time.time() - start_time:.2f}s",
                      "\033[K", end="\r", flush=True)
        RecipeTokenFrequency.objects.bulk_create(objs)
        print(f"Token {r['token']} "
              f"| Recipe {r['recipe']} "
              f"| {count} completed | {time.time() - start_time:.2f}s",
              "\033[K", end="\r", flush=True)
        print("\n\n")

    @staticmethod
    def store_recipetoken_frequency_recipe_length():
        from django.db.models import OuterRef, Subquery
        RecipeTokenFrequency.objects.all().update(
            recipe_length=Subquery(
                RecipeTokenFrequency.objects.filter(
                    pk=OuterRef('pk')).values('recipe__length')[:1]))

    def delete_rare_tokens(self):
        token_counts = RecipeToken.objects.values(
            "token").annotate(count=Count("*"))
        token_ids_to_delete = [r["token"]
                               for r in token_counts.filter(count__lte=5)]
        for token_id in token_ids_to_delete:
            Token.objects.get(id=token_id).delete()

    def calculate_recipe_frequencies(self):
        tokens = Token.objects.all()
        for token in tokens:
            token.recipe_count = token.recipes.distinct().count()
            token.save()

    @staticmethod
    def construct_spellchecker_data():
        token_counts = dict(Token.objects.annotate(token_count=Count("recipes"))
                                 .values_list("title", "token_count"))
        # Make parent directory if it doesn't exist
        SpellChecker._DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(SpellChecker._DATAFILE, "wb") as f:
            pickle.dump(token_counts, f)
