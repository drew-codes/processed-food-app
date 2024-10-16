from time import time
from django.core.management.base import BaseCommand
from scraper.scraper import run_scraper
from scraper.scraper2 import run_scraper2


class Command(BaseCommand):
    help = "Run the scraper to collect data from vendor sites"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting the scraper..."))
        start = time()
        run_scraper2(self.stdout, self.style)
        duration = time() - start
        self.stdout.write(
            self.style.SUCCESS(f"Scraper completed successfully in {duration} seconds.")
        )
