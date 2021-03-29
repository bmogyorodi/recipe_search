import nltk
from django.core.management.base import BaseCommand
from data.data_loader import *
from time import time
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Runs essential data_loader initialization methods'

    def handle(self, *args, **options):
        t0 = time()
        self.stdout.write(self.style.WARNING(
            f"Starting at {datetime.now():%H:%M:%S}"))
        # Download NLTK libraries
        self.stdout.write(self.style.WARNING("Downloading NLTK"))
        nltk.download("stopwords")
        nltk.download("wordnet")
        self.stdout.write(self.style.SUCCESS("NLTK Downloaded"))
        # Save recipe__length (dunderscore) into recipe_length
        self.stdout.write(self.style.WARNING("Saving recipe_length"))
        DataLoader.store_recipetoken_frequency_recipe_length()
        self.stdout.write(self.style.SUCCESS("recipe_length finished"))
        # Spell checker
        self.stdout.write(self.style.WARNING("Constructing spellchecker"))
        DataLoader.construct_spellchecker_data()
        self.stdout.write(self.style.SUCCESS("Spellchecker constructed"))

        # Check how long it took
        tf = time()
        delta = timedelta(seconds=tf - t0)
        self.stdout.write(self.style.SUCCESS("=" * 30))
        self.stdout.write(
            self.style.SUCCESS(f"Finishing at: {datetime.now():%H:%M:%S}"))
        self.stdout.write(
            self.style.SUCCESS(f"Total time: {delta}"))
