from django.urls import path
from .views import generate, upload, keygen

urlpatterns = [
    path("api/generate/", generate, name="Random number generator"),
    path("token/", keygen, name="token generation"),
    path("", upload, name="upload")
]