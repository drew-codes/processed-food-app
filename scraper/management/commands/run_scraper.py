from django.core.management.base import BaseCommand
from scraper.scraper import run_scraper  # Import the function that runs your scraper


class Command(BaseCommand):
    help = "Run the scraper to collect data from vendor sites"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting the scraper..."))
        run_scraper()  # Call your scraper function here
        self.stdout.write(self.style.SUCCESS("Scraper completed successfully."))
