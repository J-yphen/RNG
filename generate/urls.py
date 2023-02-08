from django.urls import path
from .views import generate, user_quota, upload, form

urlpatterns = [
    path("api/generate/", generate, name="Random number generator"),
    path("api/balance/", user_quota, name="User Quota"),
    path("token/", form, name="token generation"),
    path("", upload, name="upload"),
]