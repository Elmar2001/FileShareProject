from django.urls import path
from . import views

urlpatterns = [
    path("", views.loginRedirect, name='index'),
    path("login/", views.user_login, name='login'),
    path("logout/", views.user_logout, name='logout'),
    path("files", views.files_view, name='files'),
    path("upload", views.upload, name='upload'),
    path("Files/<str:filename>/", views.download, name='download'),
    path("share/<str:filename>/", views.share, name='share'),
    path("comment/<int:pk>", views.comment, name='comment'),
    path("view/<str:filename>", views.view, name='view')

]