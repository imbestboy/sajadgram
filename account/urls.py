from . import views

from django.urls import path
from django.contrib.auth.views import LogoutView


app_name = "account"
urlpatterns = [
    path("signup/", view=views.SignupView.as_view(), name="signup"),
    path("login/", view=views.LoginView.as_view(), name="login"),
    path("logout/", view=LogoutView.as_view(), name="logout"),
    path("", view=views.TimeLineView.as_view(), name="timeline"),
    path("edit-profile/", views.EditProfileView.as_view(), name="edit-profile"),
    path("follow/", views.FollowUnfollowView.as_view(), name="follow"),
    path("block/", views.BlockUnblockView.as_view(), name="block"),
    path("search/", views.SearchView.as_view(), name="search"),
    path(
        "finalize-signup/", views.FinalizeSignupView.as_view(), name="finalize-signup"
    ),
    path(
        "followings/<str:username>/",
        views.FollowingsListView.as_view(),
        name="followings",
    ),
    path(
        "followers/<str:username>/",
        views.FollowersListView.as_view(),
        name="followers",
    ),
    path("reset-password/", views.PasswordResetView.as_view(), name="reset-password"),
    path(
        "reset-password-done/",
        views.PasswordResetDoneView.as_view(),
        name="reset-password-done",
    ),
    path(
        "reset-password-confirm/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="reset-password-confirm",
    ),
    path(
        "reset-password-complete/",
        views.PasswordResetCompleteView.as_view(),
        name="reset-password-complete",
    ),
    path("<str:username>/", views.ProfileView.as_view(), name="profile"),
]
