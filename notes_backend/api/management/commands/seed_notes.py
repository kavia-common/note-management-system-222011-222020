from django.core.management.base import BaseCommand
from django.utils import timezone

from api.models import Note


class Command(BaseCommand):
    help = "Seed the database with sample notes if none exist."

    # PUBLIC_INTERFACE
    def handle(self, *args, **options):
        """Seed notes into the database if there are currently no notes."""
        if Note.objects.exists():
            self.stdout.write(self.style.WARNING("Notes already exist. No seeding performed."))
            return

        sample = [
            {"title": "Welcome to Notes", "content": "This is your first note. Feel free to edit or delete it."},
            {"title": "Django REST Tips", "content": "Use serializers for validation and clean APIs."},
            {"title": "Next steps", "content": "Build a frontend or integrate with other services."},
        ]
        for item in sample:
            Note.objects.create(
                title=item["title"].strip(),
                content=item["content"],
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(sample)} sample notes."))
