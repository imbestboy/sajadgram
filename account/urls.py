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
    path("<str:username>/", views.ProfileView.as_view(), name="profile"),
]
