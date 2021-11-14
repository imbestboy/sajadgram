from django.urls import path

from . import views

app_name = "post"

urlpatterns = [
    path("create-post/", views.CreatePostView.as_view(), name="create"),
    path("saved-posts/", views.SavedPostListView.as_view(), name="saved-list"),
    path("liked-posts/", views.LikedPostListView.as_view(), name="liked-list"),
    path("post/<str:display_name>", views.ShowPostView.as_view(), name="show"),
    path("posts/<str:username>/", views.UserPostList.as_view(), name="user-post-list"),
    path("save-post/", views.SaveUnsaveView.as_view(), name="save"),
]
