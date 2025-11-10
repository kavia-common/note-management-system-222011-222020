from django.urls import path
from .views import health, notes_list, notes_detail

urlpatterns = [
    # Health
    path("health/", health, name="Health"),

    # Notes CRUD
    path("notes", notes_list, name="notes-list"),            # /api/notes
    path("notes/", notes_list, name="notes-list-slash"),     # allow trailing slash
    path("notes/<int:pk>", notes_detail, name="notes-detail"),
    path("notes/<int:pk>/", notes_detail, name="notes-detail-slash"),
]
