from django.conf import settings
from django.core.management.base import BaseCommand

from khapi.cache_system.create import generate_cache_files


class Command(BaseCommand):
    help = "Run the generate_cache() function if there are any unapplied migrations."

    def handle(self, *args, **options):
        try:
            if settings.KHAPI:
                if settings.KHAPI["CACHE_APPS"]:
                    app_names = settings.KHAPI["CACHE_APPS"]
                else:
                    raise Exception("CACHE_APPS not found in settings")
            else:
                raise Exception("khapi app is not found in settings")
            generate_cache_files(app_names)
            self.stdout.write(self.style.SUCCESS("Successfully generated cache models"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
            raise e
