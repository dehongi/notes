from django.shortcuts import render

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Note
from .forms import NoteForm

# Create your views here.


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = "notes/note_list.html"
    context_object_name = "notes"
    paginate_by = 10

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by("-updated_at")


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = "notes/note_detail.html"
    context_object_name = "note"

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = "notes/note_form.html"
    success_url = reverse_lazy("notes:note_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "notes/note_form.html"
    success_url = reverse_lazy("notes:note_list")

    def test_func(self):
        note = self.get_object()
        return self.request.user == note.user


class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Note
    template_name = "notes/note_confirm_delete.html"
    success_url = reverse_lazy("notes:note_list")

    def test_func(self):
        note = self.get_object()
        return self.request.user == note.user


class PublicNoteListView(ListView):
    model = Note
    template_name = "notes/public_note_list.html"
    context_object_name = "notes"
    paginate_by = 10

    def get_queryset(self):
        return Note.objects.filter(is_public=True).order_by("-updated_at")


class PublicNoteDetailView(DetailView):
    model = Note
    template_name = "notes/public_note_detail.html"
    context_object_name = "note"

    def get_queryset(self):
        return Note.objects.filter(is_public=True)


def home_view(request):
    public_notes = Note.objects.filter(is_public=True).order_by("-updated_at")[:5]
    context = {
        "public_notes": public_notes,
    }
    return render(request, "notes/home.html", context)
