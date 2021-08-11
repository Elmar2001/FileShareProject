from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("files", views.files_view, name='files'),
    path("upload", views.upload, name='upload'),
    path("Files/<str:filename>/", views.download, name='download'),
    path("share/<str:filename>/", views.share, name='share'),


]