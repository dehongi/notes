from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
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
from django.db.models import Q
from .models import Note, Comment
from .forms import NoteForm, CommentForm
from accounts.models import CustomUser

# Create your views here.


class NoteListView(LoginRequiredMixin, ListView):
    """
    Display a list of notes that belong to the current user.

    This view restricts access to authenticated users and shows only their notes,
    sorted by most recently updated.

    Attributes:
        model: The model to query (Note)
        template_name: The template to render
        context_object_name: Variable name to use in the template
        paginate_by: Number of notes per page
    """

    model = Note
    template_name = "notes/note_list.html"
    context_object_name = "notes"
    paginate_by = 10

    def get_queryset(self):
        """
        Return the queryset of notes filtered by the current user and optional search query.

        Returns:
            QuerySet of Note objects belonging to the current user, filtered by search term if provided.
        """
        queryset = Note.objects.filter(user=self.request.user).order_by("-updated_at")

        # Handle search functionality
        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.

        Returns:
            Dict with context data including search query if present.
        """
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        return context


class NoteDetailView(LoginRequiredMixin, DetailView):
    """
    Display details of a specific note.

    This view restricts access to authenticated users and only allows viewing
    notes that belong to the current user.

    Attributes:
        model: The model to query (Note)
        template_name: The template to render
        context_object_name: Variable name to use in the template
    """

    model = Note
    template_name = "notes/note_detail.html"
    context_object_name = "note"

    def get_queryset(self):
        """
        Restrict the queryset to notes owned by the current user.

        Returns:
            QuerySet of Note objects belonging to the current user.
        """
        return Note.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Add comment form and related comments to the context.

        Returns:
            Dict with context data including comment form and active comments.
        """
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        context["comments"] = self.object.comments.filter(is_active=True)
        return context


class NoteCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new note.

    This view restricts access to authenticated users and associates the new note
    with the current user.

    Attributes:
        model: The model to create (Note)
        form_class: Form class to use for note creation
        template_name: The template to render
        success_url: URL to redirect to after successful creation
    """

    model = Note
    form_class = NoteForm
    template_name = "notes/note_form.html"
    success_url = reverse_lazy("notes:note_list")

    def form_valid(self, form):
        """
        Set the note's user to the current user before saving.

        Args:
            form: The validated form instance

        Returns:
            HttpResponse: Redirect to success URL
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update an existing note.

    This view restricts access to authenticated users and only allows editing
    notes that belong to the current user.

    Attributes:
        model: The model to update (Note)
        form_class: Form class to use for note updating
        template_name: The template to render
        success_url: URL to redirect to after successful update
    """

    model = Note
    form_class = NoteForm
    template_name = "notes/note_form.html"
    success_url = reverse_lazy("notes:note_list")

    def test_func(self):
        """
        Test if the current user is the owner of the note.

        Returns:
            bool: True if the current user is the note owner, False otherwise
        """
        note = self.get_object()
        return self.request.user == note.user


class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete an existing note.

    This view restricts access to authenticated users and only allows deleting
    notes that belong to the current user.

    Attributes:
        model: The model to delete (Note)
        template_name: The template to render for confirmation
        success_url: URL to redirect to after successful deletion
    """

    model = Note
    template_name = "notes/note_confirm_delete.html"
    success_url = reverse_lazy("notes:note_list")

    def test_func(self):
        """
        Test if the current user is the owner of the note.

        Returns:
            bool: True if the current user is the note owner, False otherwise
        """
        note = self.get_object()
        return self.request.user == note.user


class PublicNoteListView(ListView):
    """
    Display a list of all public notes.

    This view is accessible to all users and shows notes marked as public,
    sorted by most recently created.

    Attributes:
        model: The model to query (Note)
        template_name: The template to render
        context_object_name: Variable name to use in the template
        paginate_by: Number of notes per page
    """

    model = Note
    template_name = "notes/public_note_list.html"
    context_object_name = "notes"
    paginate_by = 12

    def get_queryset(self):
        """
        Return the queryset of public notes, optionally filtered by search query.

        Returns:
            QuerySet of public Note objects, filtered by search term if provided.
        """
        queryset = Note.objects.filter(is_public=True).order_by("-created_at")

        # Handle search functionality
        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add following information and search query to the context.

        Returns:
            Dict with context data including following IDs if user is authenticated,
            and search query if present.
        """
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")

        # Add following information if user is authenticated
        if self.request.user.is_authenticated:
            from accounts.models import Follow

            following_ids = Follow.objects.filter(
                follower=self.request.user
            ).values_list("followed_id", flat=True)
            context["following_ids"] = list(following_ids)

        return context


class PublicNoteDetailView(DetailView):
    """
    Display details of a specific public note.

    This view allows viewing notes marked as public and raises a 404 error
    for non-public notes.

    Attributes:
        model: The model to query (Note)
        template_name: The template to render
        context_object_name: Variable name to use in the template
    """

    model = Note
    template_name = "notes/public_note_detail.html"
    context_object_name = "note"

    def get_object(self, queryset=None):
        """
        Get the note object and verify it's marked as public.

        Raises:
            Http404: If the note is not public

        Returns:
            Note: The public note object
        """
        # Get the object and verify it's a public note
        obj = super().get_object(queryset)
        if not obj.is_public:
            raise Http404("This note is not public.")
        return obj

    def get_context_data(self, **kwargs):
        """
        Add comment form and following information to the context.

        Returns:
            Dict with context data including comment form and following IDs if user is authenticated.
        """
        context = super().get_context_data(**kwargs)

        # Add comment form
        context["comment_form"] = CommentForm()
        context["comments"] = self.object.comments.filter(is_active=True)

        # Add following information if user is authenticated
        if self.request.user.is_authenticated:
            from accounts.models import Follow

            following_ids = Follow.objects.filter(
                follower=self.request.user
            ).values_list("followed_id", flat=True)
            context["following_ids"] = list(following_ids)

        return context


def home_view(request):
    """
    Display the home page with recent public notes.

    Args:
        request: The HTTP request object

    Returns:
        HttpResponse: Rendered home page with public notes
    """
    public_notes = Note.objects.filter(is_public=True).order_by("-updated_at")[:5]
    context = {
        "public_notes": public_notes,
    }
    return render(request, "notes/home.html", context)


class PublicNotesByUserListView(ListView):
    """
    Display a list of public notes by a specific user.

    This view shows public notes from a particular user identified by their slug.

    Attributes:
        model: The model to query (Note)
        template_name: The template to render
        context_object_name: Variable name to use in the template
        paginate_by: Number of notes per page
    """

    model = Note
    template_name = "notes/public_notes_by_user.html"
    context_object_name = "notes"
    paginate_by = 9

    def get_queryset(self):
        """
        Return the queryset of public notes by the specified user.

        Returns:
            QuerySet of public Note objects belonging to the user specified by the slug.
        """
        queryset = Note.objects.filter(
            user__slug=self.kwargs["slug"], is_public=True
        ).order_by("-created_at")

        # Handle search functionality
        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add profile user, meta information, following status, and search query to the context.

        Returns:
            Dict with context data including profile user, meta information,
            following status if user is authenticated, and search query if present.
        """
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(CustomUser, slug=self.kwargs["slug"])
        context["profile_user"] = user
        context["meta"] = {
            "title": f"{user.get_full_name()}'s Public Notes",
            "description": f"Browse public notes shared by {user.get_full_name()}",
        }
        context["search_query"] = self.request.GET.get("q", "")

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
    """
    Add a comment to a note.

    This view restricts access to authenticated users and verifies that the user
    can comment on the note (either public or owned by the user).

    Args:
        request: The HTTP request object
        pk: The primary key of the note to comment on

    Returns:
        HttpResponse: Redirect to the appropriate detail view
    """
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
    """
    Delete a comment.

    This view restricts access to authenticated users and verifies that the user
    can delete the comment (either comment owner or note owner).

    Args:
        request: The HTTP request object
        pk: The primary key of the comment to delete

    Returns:
        HttpResponse: Redirect to the appropriate detail view
    """
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
    """
    Display the main home page with featured notes.

    Args:
        request: The HTTP request object

    Returns:
        HttpResponse: Rendered home page with featured notes
    """
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
