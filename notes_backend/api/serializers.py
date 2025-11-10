from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for Note model with basic validation.
    Ensures title is non-empty (after trimming whitespace).
    """

    # Enforce non-empty title
    def validate_title(self, value: str) -> str:
        if value is None or not str(value).strip():
            raise serializers.ValidationError("Title must not be empty.")
        return value.strip()

    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
