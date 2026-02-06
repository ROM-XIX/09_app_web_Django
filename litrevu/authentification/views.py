# /P_09/litrevu/authentification/views.py
"""Vues de l'app `authentification`.

Cette app fournit :
- une page de connexion (login)
- une page d'accueil (protégée) comme exemple
- une déconnexion (logout)

On utilise le système d'authentification standard de Django.
"""

from django.contrib import messages
from django.contrib.auth import logout

# from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView  # , LogoutView
from django.shortcuts import redirect, render

from .forms import SignupForm, StyledAuthenticationForm

# from django.urls import reverse_lazy


class UserLoginView(LoginView):
    """Page de connexion."""

    template_name = "login.html"
    authentication_form = StyledAuthenticationForm


# class UserLogoutView(LogoutView):
#     """Déconnexion puis redirection vers la page de connexion."""
#     next_page = reverse_lazy("login")


def logout_view(request):
    logout(request)
    return redirect("login")


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte créé avec succès. Vous pouvez vous connecter.")
            return redirect("login")
    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})
