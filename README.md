# note-management-system-222011-222020

Backend: Django + Django REST Framework
Docs: Visit /docs for Swagger UI once the server is running.

## Notes API

Base path: /api

Resources:
- GET /api/notes?page=1&page_size=10&ordering=-updated_at
- POST /api/notes
- GET /api/notes/<id>
- PUT /api/notes/<id>
- PATCH /api/notes/<id>
- DELETE /api/notes/<id>

Default ordering is -updated_at. Allowed ordering values: updated_at, -updated_at.
Pagination params:
- page (default 1)
- page_size (default 10, max 100)

### curl examples

Health:
curl -sS http://localhost:3001/api/health/

List notes:
curl -sS "http://localhost:3001/api/notes?page=1&page_size=5"

Create a note:
curl -sS -X POST http://localhost:3001/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"My first note","content":"Hello world"}'

Get a note:
curl -sS http://localhost:3001/api/notes/1

Update a note (PUT):
curl -sS -X PUT http://localhost:3001/api/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated title","content":"Updated content"}'

Partial update (PATCH):
curl -sS -X PATCH http://localhost:3001/api/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Patched title"}'

Delete a note:
curl -sS -X DELETE http://localhost:3001/api/notes/1 -i

### Status codes
- 200 OK: Successful read/update
- 201 Created: Successful create
- 204 No Content: Successful delete
- 400 Bad Request: Validation errors (e.g., empty title)
- 404 Not Found: Note does not exist

## Seeding data
To add sample notes when the database is empty, run:
python notes_backend/manage.py migrate
python notes_backend/manage.py seed_notes

This will create a few sample notes if none are found.