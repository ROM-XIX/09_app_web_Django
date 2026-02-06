# /P_09/litrevu/authentification/urls.py
from django.shortcuts import redirect
from django.urls import path  # , reverse_lazy

from .views import UserLoginView, logout_view, signup  # , UserLogoutView


def root(request):
    if request.user.is_authenticated:
        return redirect("feed")  # si login alors on redirige vers /flux/
    return redirect("login")  # si pas login alors on redirige vers /login/


urlpatterns = [
    path("", root, name="root"),
    path("login/", UserLoginView.as_view(), name="login"),
    # path("logout/", UserLogoutView.as_view(), name="logout"),
    path("logout/", logout_view, name="logout"),
    path("signup/", signup, name="signup"),
]
