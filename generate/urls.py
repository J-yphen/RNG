from django.urls import path
from .views import generate, upload

urlpatterns = [
    path("api/generate/", generate, name="generate"),
    path("", upload, name="upload")
]