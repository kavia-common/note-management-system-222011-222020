from django.db import models


class Note(models.Model):
    """
    Note model representing a simple note entity with title and content.
    Stores timestamps for creation and updates.
    """
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ("-updated_at",)

    def __str__(self) -> str:
        return f"{self.id}: {self.title[:50]}"
