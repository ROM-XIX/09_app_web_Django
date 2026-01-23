from django.shortcuts import redirect
from django.urls import path

from .views import UserLoginView, UserLogoutView, home, signup


def root(request):
    return redirect("home")  # ou redirect("login") si tu préfères


urlpatterns = [
    path("", root, name="root"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("home/", home, name="home"),
    path("signup/", signup, name="signup"),
]
