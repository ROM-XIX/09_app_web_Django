from django import forms

from .models import Review, Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["headline", "body", "rating"]
        widgets = {
            "rating": forms.RadioSelect(choices=[(i, str(i)) for i in range(6)]),
        }


class TicketReviewForm(forms.Form):
    """Form combiné pour créer un Ticket + une Review en une seule étape."""

    title = forms.CharField(max_length=128)
    description = forms.CharField(required=False, widget=forms.Textarea)
    image = forms.ImageField(required=False)

    headline = forms.CharField(max_length=128)
    body = forms.CharField(required=False, widget=forms.Textarea)
    rating = forms.ChoiceField(choices=[(i, str(i)) for i in range(6)], widget=forms.RadioSelect)

    def clean_rating(self):
        return int(self.cleaned_data["rating"])
