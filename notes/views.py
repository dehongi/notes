from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Note, Comment
from .forms import NoteForm, CommentForm
from accounts.models import CustomUser

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        context["comments"] = self.object.comments.filter(is_active=True)
        return context


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
    paginate_by = 12

    def get_queryset(self):
        return Note.objects.filter(is_public=True).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add following information if user is authenticated
        if self.request.user.is_authenticated:
            from accounts.models import Follow

            following_ids = Follow.objects.filter(
                follower=self.request.user
            ).values_list("followed_id", flat=True)
            context["following_ids"] = list(following_ids)

        return context


class PublicNoteDetailView(DetailView):
    model = Note
    template_name = "notes/public_note_detail.html"
    context_object_name = "note"

    def get_object(self, queryset=None):
        # Get the object and verify it's a public note
        obj = super().get_object(queryset)
        if not obj.is_public:
            raise Http404("This note is not public.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add comment form
        context["comment_form"] = CommentForm()

        # Add following information if user is authenticated
        if self.request.user.is_authenticated:
            from accounts.models import Follow

            following_ids = Follow.objects.filter(
                follower=self.request.user
            ).values_list("followed_id", flat=True)
            context["following_ids"] = list(following_ids)

        return context


def home_view(request):
    public_notes = Note.objects.filter(is_public=True).order_by("-updated_at")[:5]
    context = {
        "public_notes": public_notes,
    }
    return render(request, "notes/home.html", context)


class PublicNotesByUserListView(ListView):
    model = Note
    template_name = "notes/public_notes_by_user.html"
    context_object_name = "notes"
    paginate_by = 9

    def get_queryset(self):
        return Note.objects.filter(
            user__slug=self.kwargs["slug"], is_public=True
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(CustomUser, slug=self.kwargs["slug"])
        context["profile_user"] = user
        context["meta"] = {
            "title": f"{user.get_full_name()}'s Public Notes",
            "description": f"Browse public notes shared by {user.get_full_name()}",
        }

        # Add following information if user is authenticated
        if self.request.user.is_authenticated:
            from accounts.models import Follow

            # Check if current user is following the profile user
            context["is_following"] = Follow.objects.filter(
                follower=self.request.user, followed=user
            ).exists()

            # Get all users the current user is following for other note authors
            following_ids = Follow.objects.filter(
                follower=self.request.user
            ).values_list("followed_id", flat=True)
            context["following_ids"] = list(following_ids)

        return context


@login_required
def add_comment(request, pk):
    note = get_object_or_404(Note, pk=pk)

    # Check if the note is public or if the current user is the owner
    if not note.is_public and note.user != request.user:
        messages.error(request, "You cannot comment on this note.")
        return redirect("notes:note_list")

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.note = note
            comment.user = request.user
            comment.save()
            messages.success(request, "Your comment has been posted.")

            # Redirect to the appropriate detail view
            if note.user == request.user:
                return redirect("notes:note_detail", pk=note.pk)
            else:
                return redirect("notes:public_note_detail", pk=note.pk)

    # If GET request or form invalid, redirect back
    messages.error(request, "Error posting comment.")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    note = comment.note

    # Check if user is the comment owner or note owner
    if request.user != comment.user and request.user != note.user:
        messages.error(request, "You cannot delete this comment.")
        return redirect("notes:note_list")

    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted successfully.")

    # Redirect to the appropriate detail view
    if note.user == request.user:
        return redirect("notes:note_detail", pk=note.pk)
    else:
        return redirect("notes:public_note_detail", pk=note.pk)


def index(request):
    """Home page view."""
    # Get featured notes for homepage
    featured_notes = Note.objects.filter(is_public=True).order_by("-created_at")[:6]

    context = {
        "featured_notes": featured_notes,
    }

    # Add following information if user is authenticated
    if request.user.is_authenticated:
        from accounts.models import Follow

        following_ids = Follow.objects.filter(follower=request.user).values_list(
            "followed_id", flat=True
        )
        context["following_ids"] = list(following_ids)

    return render(request, "website/home.html", context)
