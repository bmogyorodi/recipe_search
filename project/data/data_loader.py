from .indexer import Indexer
from pathlib import Path
import pickle
import bz2
import os
import time
from data.models import Recipe


class DataLoader():
    _RAW_DATA_DIR = Path(__file__).parent.resolve() / "data"

    def __init__(self, files_to_load=None):
        self.indexer = Indexer()
        self.filenames = [fn for fn in os.listdir(self._RAW_DATA_DIR) if fn.split(".")[-1] == "pbz2"]
        if files_to_load is not None:
            self.filenames = [fn for fn in self.filenames if fn in files_to_load]

    def import_datasets(self):
        for filename in self.filenames:
            self._import_dataset(filename)

    def _import_dataset(self, filename):
        source = filename.split(".")[0]
        recipes = self._load_datafile(filename)["recipes"]
        start_time = time.time()

        print("------------------------------------")
        print(f"Indexing {source}")
        print("------------------------------------")
        print(f"Recipes already indexed: {len(Recipe.objects.filter(source=source))}")
        print(f"New recipes to index:    {len(recipes) - len(Recipe.objects.filter(source=source))}")
        print()

        count = 0
        for source_id, recipe in recipes.items():
            # If recipe is not already in the database, add it
            if len(recipe["ingredients"]) > 0 and len(recipe["instructions"]) > 0 \
               and not Recipe.objects.filter(source=source, source_id=source_id):

                recipe_obj = Recipe(title=recipe["title"],
                                    canonical_url=recipe["canonical_url"],
                                    image=recipe["image"],
                                    author=recipe["author"],
                                    source=source,
                                    source_id=source_id,
                                    ratings=recipe.get("ratings", -1),
                                    total_time=recipe.get("total_time", 0),
                                    yields=recipe.get("yields", ""),
                                    **recipe.get("nutrients", {}))
                recipe_obj.save()

                recipe_text = {
                    "title": recipe["title"],
                    "ingredients": " ".join(recipe["ingredients"]),
                    "instructions": recipe["instructions"],
                    "author": recipe["author"]
                }
                self.indexer.index_recipe(recipe_obj, recipe_text)

                count += 1
                print(f"Imported {count} recipes | Total Time: {time.time() - start_time:.2f}s | Current recipe ID: {source_id}", "\033[K", end="\r", flush=True)
        print("\n\n")

    def _load_datafile(self, filename):
        with bz2.BZ2File(self._RAW_DATA_DIR / filename, "rb") as f:
            return pickle.load(f)
