from django.urls import path
from . import views

app_name = "notes"

urlpatterns = [
    path("", views.NoteListView.as_view(), name="note_list"),
    path("<int:pk>/", views.NoteDetailView.as_view(), name="note_detail"),
    path("create/", views.NoteCreateView.as_view(), name="note_create"),
    path("<int:pk>/update/", views.NoteUpdateView.as_view(), name="note_update"),
    path("<int:pk>/delete/", views.NoteDeleteView.as_view(), name="note_delete"),
    path("public/", views.PublicNoteListView.as_view(), name="public_note_list"),
    path(
        "public/<int:pk>/",
        views.PublicNoteDetailView.as_view(),
        name="public_note_detail",
    ),
    path(
        "public/user/<str:slug>/",
        views.PublicNotesByUserListView.as_view(),
        name="public_notes_by_user",
    ),
    path("<int:pk>/comment/", views.add_comment, name="add_comment"),
    path("comment/<int:pk>/delete/", views.delete_comment, name="delete_comment"),
]
