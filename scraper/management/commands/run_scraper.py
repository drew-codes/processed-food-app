from django.core.management.base import BaseCommand
from scraper.scraper import run_scraper


class Command(BaseCommand):
    help = "Run the scraper to collect data from vendor sites"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting the scraper..."))
        run_scraper()
        self.stdout.write(self.style.SUCCESS("Scraper completed successfully."))
