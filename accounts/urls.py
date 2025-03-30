from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    # Password reset
    path(
        "password-reset/",
        views.CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        views.CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset/confirm/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        views.CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # Password change
    path(
        "password-change/",
        views.CustomPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password-change/done/",
        views.CustomPasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    # Profile
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/edit/", views.ProfileUpdateView.as_view(), name="profile_edit"),
    path(
        "profile/public/<str:slug>/",
        views.PublicProfileView.as_view(),
        name="public_profile",
    ),
    # Following System
    path("follow/<str:slug>/", views.follow_user, name="follow"),
    path("unfollow/<str:slug>/", views.unfollow_user, name="unfollow"),
    path(
        "profile/<str:slug>/followers/",
        views.FollowersListView.as_view(),
        name="followers",
    ),
    path(
        "profile/<str:slug>/following/",
        views.FollowingListView.as_view(),
        name="following",
    ),
]
