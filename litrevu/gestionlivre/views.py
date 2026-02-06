# litrevu/gestionlivre/views.py
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReviewForm, TicketForm, TicketReviewForm
from .models import Review, Ticket


@login_required
def ticket_create(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("feed")  # adapte si ton flux s'appelle autrement
    else:
        form = TicketForm()
    return render(request, "gestionlivre/ticket_form.html", {"form": form})


@login_required
def review_create_for_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    # (Optionnel) empêcher de répondre deux fois au même ticket (souvent demandé)
    if Review.objects.filter(ticket=ticket, user=request.user).exists():
        return redirect("feed")

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect("feed")
    else:
        form = ReviewForm()

    return render(
        request,
        "gestionlivre/review_form_for_ticket.html",
        {"form": form, "ticket": ticket},
    )


@login_required
@transaction.atomic
def ticket_and_review_create(request):
    """Crée un ticket + une review en une seule étape (review from scratch)."""
    if request.method == "POST":
        form = TicketReviewForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = Ticket.objects.create(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                image=form.cleaned_data.get("image"),
                user=request.user,
            )
            Review.objects.create(
                ticket=ticket,
                rating=form.cleaned_data["rating"],
                user=request.user,
                headline=form.cleaned_data["headline"],
                body=form.cleaned_data["body"],
            )
            return redirect("feed")
    else:
        form = TicketReviewForm()

    return render(request, "gestionlivre/ticket_review_form.html", {"form": form})
