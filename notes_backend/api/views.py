from typing import Any
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request

from .models import Note
from .serializers import NoteSerializer


# PUBLIC_INTERFACE
@api_view(["GET"])
def health(request: Request) -> Response:
    """Health check endpoint that returns a static message."""
    return Response({"message": "Server is up!"})


def _paginate_queryset(qs: QuerySet, request: Request) -> dict[str, Any]:
    """
    Apply simple pagination based on query parameters:
    - page (default 1)
    - page_size (default 10, max 100)

    Returns a dict with pagination metadata and the sliced queryset list.
    """
    try:
        page = max(1, int(request.query_params.get("page", 1)))
    except (TypeError, ValueError):
        page = 1
    try:
        page_size = int(request.query_params.get("page_size", 10))
    except (TypeError, ValueError):
        page_size = 10
    page_size = max(1, min(page_size, 100))

    total = qs.count()
    start = (page - 1) * page_size
    end = start + page_size
    items = qs[start:end]

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "results": items,
    }


# PUBLIC_INTERFACE
@api_view(["GET", "POST"])
def notes_list(request: Request) -> Response:
    """
    List and create notes.

    GET /notes
    - Returns paginated list of notes ordered by -updated_at by default.
    - Query params:
      - page: int (default 1)
      - page_size: int (default 10, max 100)
      - ordering: field to order by, supports 'updated_at' and '-updated_at' (default: -updated_at)

    POST /notes
    - Body: {"title": "<non-empty>", "content": "<string optional>"}
    - Returns 201 with created note or 400 with validation errors.
    """
    if request.method == "GET":
        ordering = request.query_params.get("ordering", "-updated_at")
        if ordering not in ("updated_at", "-updated_at"):
            ordering = "-updated_at"
        qs = Note.objects.all().order_by(ordering)
        page_data = _paginate_queryset(qs, request)
        serializer = NoteSerializer(page_data["results"], many=True)
        return Response(
            {
                "page": page_data["page"],
                "page_size": page_data["page_size"],
                "total": page_data["total"],
                "results": serializer.data,
                "ordering": ordering,
            },
            status=status.HTTP_200_OK,
        )

    # POST
    serializer = NoteSerializer(data=request.data)
    if serializer.is_valid():
        note = serializer.save()
        out = NoteSerializer(note)
        return Response(out.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PUBLIC_INTERFACE
@api_view(["GET", "PUT", "PATCH", "DELETE"])
def notes_detail(request: Request, pk: int) -> Response:
    """
    Retrieve, update, or delete a note by id.

    GET /notes/<id> -> 200 with note or 404
    PUT/PATCH /notes/<id> -> 200 with updated note or 400 validation errors
    DELETE /notes/<id> -> 204 on success
    """
    note = get_object_or_404(Note, pk=pk)

    if request.method == "GET":
        serializer = NoteSerializer(note)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method in ("PUT", "PATCH"):
        partial = request.method == "PATCH"
        serializer = NoteSerializer(note, data=request.data, partial=partial)
        if serializer.is_valid():
            updated = serializer.save()
            return Response(NoteSerializer(updated).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    note.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
