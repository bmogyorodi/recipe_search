import re
import pickle
import os
import html
from pathlib import Path
from datetime import datetime
import bz2
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords


class Indexer:
    _INDEXER_DATA_DIR = Path(__file__).parent.resolve() / "indexer_data"
    _RAW_DATA_DIR = Path(__file__).parent.resolve() / "data"
    INDEX_FILE = _INDEXER_DATA_DIR / 'index.pbz2'
    DOC_UID_FILE = _INDEXER_DATA_DIR / 'doc_uids.pbz2'
    INDEXED_DOCS_FILE = _INDEXER_DATA_DIR / 'indexed_docs.pbz2'

    def __init__(self):
        self._stopwords = stopwords.words('english')
        self._token_re = re.compile(r'[a-z\']+')
        self._wnl = WordNetLemmatizer()
        self.index = None
        self.doc_uids = None
        self.indexed_docs = None
        self._load_indexer_files()

    def _preprocess_recipe(self, recipe):
        """
        Converts recipe text to lowercase, tokenises, removes stopwords and lemmatizes the tokens
        """
        text = recipe['title']
        text += ' ' + recipe.get('author', '') if recipe.get('author', '') is not None else ''
        text += ' ' + recipe['instructions']
        text += ' ' + ' '.join(recipe['ingredients'])
        text = html.unescape(text.replace('&amp;', '&'))
        return [self._wnl.lemmatize(token.strip("'")) for token in self._token_re.findall(text.lower())
                if token.strip("'") and token.strip("'") not in self._stopwords]

    def construct_index(self, dataset_num_limit=None):
        start_time = datetime.now()
        filenames = os.listdir(self._RAW_DATA_DIR)[:dataset_num_limit]
        if len(self.doc_uids) > 0:
            uid = max(self.doc_uids.keys())
        else:
            uid = 0

        for filename in filenames:
            dataset_name = filename.split(".")[0]
            recipes = self._load_datafile(filename)['recipes']
            recipe_ids_already_indexed = self.indexed_docs.get(dataset_name, {})
            recipe_ids = recipes.keys() - recipe_ids_already_indexed

            print("------------------------------------")
            print(f"Indexing {dataset_name}")
            print("------------------------------------")
            print(f"Recipes already indexed: {len(recipe_ids_already_indexed)}")
            print(f"New recipes to index:    {len(recipe_ids)}")
            print()

            for recipe_id in recipe_ids:
                try:
                    uid += 1
                    recipe = recipes[recipe_id]
                    tokens = self._preprocess_recipe(recipe)

                    self.doc_uids[uid] = (dataset_name, recipe_id)
                    if dataset_name not in self.indexed_docs.keys():
                        self.indexed_docs[dataset_name] = {recipe_id}
                    else:
                        self.indexed_docs[dataset_name].add(recipe_id)

                    for pos in range(len(tokens)):
                        token = tokens[pos]
                        if token in self.index.keys():
                            # The token already exists in the index
                            if self.index[token][-1][0] == uid:
                                # The current document already appears in the index for the current token
                                self.index[token][-1][1].append(pos)
                            else:
                                # The current document does not appear in the index for the current token
                                self.index[token][0] += 1  # Increment document frequency
                                self.index[token].append((uid, [pos]))
                        else:
                            # The token does not currently exist in the index, add it
                            self.index[token] = [1, (uid, [pos])]
                except KeyboardInterrupt:
                    print("Saving index...")
                    self._save_indexer_files()
                    return
            self._save_indexer_files()

        print(f"TOTAL TIME: {round((datetime.now() - start_time).total_seconds())}s")

    def _load_indexer_files(self):
        if self.INDEX_FILE.exists():
            with bz2.BZ2File(self.INDEX_FILE, "rb") as f:
                self.index = pickle.load(f)
        else:
            self.index = {}

        if self.DOC_UID_FILE.exists():
            with bz2.BZ2File(self.DOC_UID_FILE, "rb") as f:
                self.doc_uids = pickle.load(f)
        else:
            self.doc_uids = {}

        if self.INDEXED_DOCS_FILE.exists():
            with bz2.BZ2File(self.INDEXED_DOCS_FILE, "rb") as f:
                self.indexed_docs = pickle.load(f)
        else:
            self.indexed_docs = {}

    def _save_indexer_files(self):
        with bz2.BZ2File(self.INDEX_FILE, "wb") as f:
            pickle.dump(self.index, f)
        with bz2.BZ2File(self.DOC_UID_FILE, "wb") as f:
            pickle.dump(self.doc_uids, f)
        with bz2.BZ2File(self.INDEXED_DOCS_FILE, "wb") as f:
            pickle.dump(self.indexed_docs, f)

    def _load_datafile(self, filename):
        with bz2.BZ2File(self._RAW_DATA_DIR / filename, "rb") as f:
            return pickle.load(f)


if __name__ == "__main__":
    indexer = Indexer()
    indexer.construct_index()
