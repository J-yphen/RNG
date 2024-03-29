from django.urls import path, re_path
from .views import generate, user_quota, form, upload

urlpatterns = [
    path("api/generate/", generate, name="Random number generator"),
    path("api/upload/", upload, name="File upload"),
    path("api/balance/", user_quota, name="User Quota"),
    re_path(r'^(?!captcha/).*$', form, name="token generation"),
]