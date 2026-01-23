"""Formulaires liés à l'authentification.

On customise légèrement le formulaire Django par défaut pour :
- avoir des placeholders
- ajouter des classes CSS (facultatif mais pratique)
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm


class StyledAuthenticationForm(AuthenticationForm):
    """Formulaire de connexion avec widgets stylés."""

    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "username",
                "placeholder": "Votre nom d'utilisateur",
                "class": "form-control",
            }
        ),
    )
    password = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "Votre mot de passe",
                "class": "form-control",
            }
        ),
    )
