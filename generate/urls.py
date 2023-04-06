from django.urls import path, re_path
from .views import generate, user_quota, form

urlpatterns = [
    path("api/generate/", generate, name="Random number generator"),
    path("api/balance/", user_quota, name="User Quota"),
    re_path(r'^(?!captcha/).*$', form, name="token generation"),
    # path("", form, name="token generation"),
    # path('*', upload, name="token generation"),
    # path("", upload, name="upload"),
]