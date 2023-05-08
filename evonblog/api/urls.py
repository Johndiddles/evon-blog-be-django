from django.urls import path
from . import views

urlpatterns = [
    path('get-posts/', views.getPosts),
    path("create-post", views.createPost),
    path("edit-post/<str:pk>", views.editPost),
    path("delete-post/<str:pk>", views.deletePost),
    path('create-user', views.createUser),
    path("login", views.loginUser),
    path("get-users", views.getUsers),
    path("add-comment", views.createComment),
    path("get-comments/<str:pk>", views.getComments),
    path("edit-comment/<str:pk>", views.editComment),
    path("edit-comment/<str:pk>", views.deleteComment),
    # path("get-posts", views.getPosts)
]