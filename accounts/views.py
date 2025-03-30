from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView,
)

from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    CustomPasswordChangeForm,
    ProfileUpdateForm,
)
from .models import CustomUser, Follow


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, "Your account has been created! You can now log in."
        )
        return response


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "accounts/login.html"

    def form_valid(self, form):
        # Form is valid, so now the authentication is done and user is about to be logged in
        response = super().form_valid(form)
        # Now the user is logged in and self.request.user is set
        if self.request.user.first_name:
            messages.success(
                self.request, f"Welcome back, {self.request.user.first_name}!"
            )
        else:
            messages.success(self.request, "Welcome back!")
        return response


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "You have been logged out.")
        return super().dispatch(request, *args, **kwargs)


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.html"
    subject_template_name = "accounts/password_reset_subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:password_change_done")


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "accounts/password_change_done.html"


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "accounts/profile.html"
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta"] = {
            "title": "Profile",
            "description": "View your profile information",
            "viewport": "width=device-width, initial-scale=1.0",
        }
        context["notes_count"] = self.object.notes.count()
        context["public_notes_count"] = self.object.notes.filter(is_public=True).count()
        return context

    def get_object(self):
        return self.request.user


class PublicProfileView(DetailView):
    model = CustomUser
    template_name = "accounts/public_profile.html"
    context_object_name = "profile_user"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add meta information
        context["meta"] = {
            "title": f"{self.object.get_full_name()}'s Profile",
            "description": f"View {self.object.get_full_name()}'s public notes",
            "viewport": "width=device-width, initial-scale=1.0",
        }

        # Add notes information
        context["public_notes"] = self.object.notes.filter(is_public=True)
        context["public_notes_count"] = context["public_notes"].count()

        # Add following information
        if self.request.user.is_authenticated:
            context["is_following"] = self.request.user.is_following(self.object)

        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = "accounts/profile_update.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated!")
        return super().form_valid(form)


@login_required
def follow_user(request, slug):
    user_to_follow = get_object_or_404(CustomUser, slug=slug)

    # Don't allow users to follow themselves
    if request.user == user_to_follow:
        messages.error(request, "You cannot follow yourself.")
        return redirect("accounts:public_profile", slug=slug)

    # Check if already following
    if not request.user.is_following(user_to_follow):
        Follow.objects.create(follower=request.user, followed=user_to_follow)
        messages.success(
            request, f"You are now following {user_to_follow.get_full_name()}."
        )
    else:
        messages.info(
            request, f"You are already following {user_to_follow.get_full_name()}."
        )

    # Handle AJAX requests
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse(
            {
                "status": "success",
                "is_following": True,
                "follower_count": user_to_follow.follower_count(),
            }
        )

    return redirect("accounts:public_profile", slug=slug)


@login_required
def unfollow_user(request, slug):
    user_to_unfollow = get_object_or_404(CustomUser, slug=slug)

    # Try to find and delete the Follow relationship
    follow = Follow.objects.filter(
        follower=request.user, followed=user_to_unfollow
    ).first()
    if follow:
        follow.delete()
        messages.success(
            request, f"You have unfollowed {user_to_unfollow.get_full_name()}."
        )
    else:
        messages.info(
            request, f"You were not following {user_to_unfollow.get_full_name()}."
        )

    # Handle AJAX requests
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse(
            {
                "status": "success",
                "is_following": False,
                "follower_count": user_to_unfollow.follower_count(),
            }
        )

    return redirect("accounts:public_profile", slug=slug)


class FollowersListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "accounts/followers_list.html"
    context_object_name = "followers"
    paginate_by = 20

    def get_queryset(self):
        self.user = get_object_or_404(CustomUser, slug=self.kwargs["slug"])
        follower_ids = Follow.objects.filter(followed=self.user).values_list(
            "follower_id", flat=True
        )
        return CustomUser.objects.filter(id__in=follower_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = self.user

        # Add is_following status for each follower if the user is authenticated
        if self.request.user.is_authenticated:
            following_ids = Follow.objects.filter(
                follower=self.request.user
            ).values_list("followed_id", flat=True)
            context["following_ids"] = list(following_ids)

        return context


class FollowingListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "accounts/following_list.html"
    context_object_name = "following"
    paginate_by = 20

    def get_queryset(self):
        self.user = get_object_or_404(CustomUser, slug=self.kwargs["slug"])
        following_ids = Follow.objects.filter(follower=self.user).values_list(
            "followed_id", flat=True
        )
        return CustomUser.objects.filter(id__in=following_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = self.user

        # Add is_following status for each followed user if the user is authenticated
        if self.request.user.is_authenticated:
            following_ids = Follow.objects.filter(
                follower=self.request.user
            ).values_list("followed_id", flat=True)
            context["following_ids"] = list(following_ids)

        return context
