from django.urls import path
from .views import *
urlpatterns = [
    path("register/",SignUpView.as_view(),name="signup"),
    path("login/",SignInView.as_view(),name="signin"),
    path("index/",IndexView.as_view(),name="index"),
    path("posts/<int:id>/comment/add",add_comments,name="add-comments"),
    path("post/<int:id>/like/add",like_post_view,name="add-like"),
    path("addpost",AddPost.as_view(),name="addpost"),
    path("people/", ListPeopleView.as_view(), name="people"),
    path("user/<int:id>/follower/add", add_follower, name="add-follower"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("post/update/",edit_profile,name="edit-profile"),
    path("profile/add/",AddProfileView.as_view(),name="profilepic"),
    path("profile/<int:id>/edit/",EditprofileView.as_view(),name="edit-pic"),
    path("post/<int:id>/remove",profile_delete_view,name="post-delete"),
    path("comment/<int:id>/remove",comment_delete,name="comment-delete"),
    path("logout",signout_view,name="logout")
]
