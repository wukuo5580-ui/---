from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("posts/", views.post_list, name="post_list"),
    path("posts/add/", views.add_post, name="add_post"),
    path("posts/<int:pk>/", views.post_detail, name="post_detail"),
    path("posts/<int:pk>/like/", views.toggle_like, name="toggle_like"),
]