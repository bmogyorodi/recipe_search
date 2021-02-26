from .indexer import Indexer
from pathlib import Path
import pickle
import bz2
import os
import time
from data.models import Recipe, Source


class DataLoader():
    _RAW_DATA_DIR = Path(__file__).parent.resolve() / "data"
    SOURCE_INFO_FILENAME = "sources.psv"

    def __init__(self, files_to_load=None):
        self.indexer = Indexer()
        self.filenames = [fn for fn in os.listdir(self._RAW_DATA_DIR) if fn.split(".")[-1] == "pbz2"]
        if files_to_load is not None:
            self.filenames = [fn for fn in self.filenames if fn in files_to_load]

    def import_datasets(self):
        for filename in self.filenames:
            try:
                self._import_dataset(filename)
            except KeyboardInterrupt:
                print("\nStopping...")
                return

    def _import_dataset(self, filename):
        source = filename.split(".")[0]
        recipes = self._load_datafile(filename)["recipes"]
        start_time = time.time()

        already_indexed = set(r.source_id for r in Recipe.objects.filter(source=source))

        print("------------------------------------")
        print(f"Indexing {source}")
        print("------------------------------------")
        print(f"Recipes already indexed: {len(already_indexed)}")
        print(f"New recipes to index:    {len(recipes) - len(already_indexed)}\n")

        count = 0
        for source_id in recipes.keys() - already_indexed:
            # If recipe is not already in the database, add it
            recipe = recipes[source_id]
            if len(recipe["ingredients"]) > 0 and len(recipe["instructions"]) > 0 \
               and not Recipe.objects.filter(source=source, source_id=source_id):

                # Remove empty "value" attribute in nutrients if it exists
                nutrients = recipe.get("nutrients", {})
                if "value" in nutrients:
                    del nutrients["value"]

                recipe_obj = Recipe(title=recipe["title"],
                                    canonical_url=recipe["canonical_url"],
                                    image=recipe["image"] if recipe["image"] is not None else "",
                                    author=recipe["author"],
                                    source=source,
                                    source_id=source_id,
                                    ratings=recipe.get("ratings", -1),
                                    total_time=recipe.get("total_time", 0),
                                    yields=recipe.get("yields", ""),
                                    **nutrients)
                recipe_obj.save()

                recipe_text = {
                    "title": recipe["title"],
                    "ingredients": " ".join(recipe["ingredients"]),
                    "instructions": recipe["instructions"],
                    "author": recipe["author"] if recipe["author"] is not None else ""
                }
                self.indexer.index_recipe(recipe_obj, recipe_text)

                count += 1
                total_time = time.time() - start_time
                print(f" Imported {count} recipes |"
                      f" Total Time: {total_time:.2f}s |"
                      f" Average Time: {total_time / count:.2f}s |"
                      f" Current recipe ID: {source_id}", "\033[K", end="\r", flush=True)
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
                source_id, source_name, source_url, favicon_url = line.split("|")
                Source.objects.get_or_create(source_id=source_id, title=source_name, url=source_url, favicon=favicon_url)
        print(f"Imported information about {count} sources")
