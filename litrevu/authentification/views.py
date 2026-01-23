"""Vues de l'app `authentification`.

Cette app fournit :
- une page de connexion (login)
- une page d'accueil (protégée) comme exemple
- une déconnexion (logout)

On utilise le système d'authentification standard de Django.
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import StyledAuthenticationForm


@login_required
def home(request):
    """Page d'exemple protégée : accessible uniquement aux utilisateurs connectés."""
    return render(request, "home.html")


class UserLoginView(LoginView):
    """Page de connexion."""

    template_name = "login.html"
    authentication_form = StyledAuthenticationForm


class UserLogoutView(LogoutView):
    """Déconnexion puis redirection vers la page de connexion."""

    next_page = reverse_lazy("login")
