from django.urls import path
from .views import generate, upload, keygen, form

urlpatterns = [
    path("api/generate/", generate, name="Random number generator"),
    path("token/", keygen, name="token generation"),
    path("", upload, name="upload"),
    path("form/", form, name="Key Generation Form")
]