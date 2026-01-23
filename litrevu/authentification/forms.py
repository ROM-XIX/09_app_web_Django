"""Formulaires liés à l'authentification.

On customise légèrement le formulaire Django par défaut pour :
- avoir des placeholders
- ajouter des classes CSS (facultatif mais pratique)
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


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


class SignupForm(UserCreationForm):
    first_name = forms.CharField(label="Prénom")
    last_name = forms.CharField(label="Nom")
    email = forms.EmailField(label="Email")
    age = forms.IntegerField(label="Âge", min_value=0)
    langue = forms.CharField(label="Langue")

    class Meta:
        model = User
        fields = (
            "username",  # alias
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                age=self.cleaned_data["age"],
                langue=self.cleaned_data["langue"],
            )
        return user
