from django.urls import path
from .views import generate, upload, keygen, form

urlpatterns = [
    path("api/generate/", generate, name="Random number generator"),
    path("token/", form, name="token generation"),
    path("", upload, name="upload"),
]