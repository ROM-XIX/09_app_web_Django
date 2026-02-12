# litrevu/gestionlivre/views.py
# Create your views here.
from itertools import chain

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import CharField, Value
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FollowUserForm, ReviewForm, TicketForm, TicketReviewForm
from .models import Review, Ticket, UserFollows


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
    return render(request, "gestionlivre/ticket_form.html", {"form": form, "mode": "create"})


@login_required
def ticket_update(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id, user=request.user)

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre billet a été modifié.")
            return redirect("posts")
    else:
        form = TicketForm(instance=ticket)

    return render(
        request,
        "gestionlivre/ticket_form.html",
        {"form": form, "mode": "update", "ticket": ticket},
    )


@login_required
def ticket_delete(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id, user=request.user)

    if request.method == "POST":
        ticket.delete()
        messages.success(request, "Votre billet a été supprimé.")
        return redirect("posts")

    return render(request, "gestionlivre/ticket_confirm_delete.html", {"ticket": ticket})


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
def review_update(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre critique a été modifiée.")
            return redirect("posts")
    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        "gestionlivre/review_form.html",
        {"form": form, "review": review},
    )


@login_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)

    if request.method == "POST":
        review.delete()
        messages.success(request, "Votre critique a été supprimée.")
        return redirect("posts")

    return render(request, "gestionlivre/review_confirm_delete.html", {"review": review})


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


def get_followed_user_ids(user):
    return UserFollows.objects.filter(user=user).values_list("followed_user_id", flat=True)


@login_required
def feed(request):
    followed_user_ids = list(get_followed_user_ids(request.user))

    # Tickets visibles = ceux des suivis + les siens
    tickets = (
        Ticket.objects.filter(user_id__in=followed_user_ids + [request.user.id])
        .select_related("user")
        .annotate(content_type=Value("TICKET", output_field=CharField()))
    )

    # Reviews visibles =
    # - reviews des suivis + les siennes
    # - + reviews en réponse à TES tickets (même si l'auteur n'est pas suivi)
    reviews = Review.objects.filter(user_id__in=followed_user_ids + [request.user.id]) | Review.objects.filter(
        ticket__user=request.user
    )
    reviews = (
        reviews.distinct()
        .select_related("user", "ticket", "ticket__user")
        .annotate(content_type=Value("REVIEW", output_field=CharField()))
    )

    posts = sorted(
        chain(tickets, reviews),
        key=lambda p: p.time_created,
        reverse=True,
    )

    return render(request, "gestionlivre/feed.html", {"posts": posts})


def home_redirect(request):
    return redirect("feed")


@login_required
def posts(request):
    """Affiche les tickets + reviews de l'utilisateur connecté (triés)."""
    tickets = (
        Ticket.objects.filter(user=request.user)
        .select_related("user")
        .annotate(content_type=Value("TICKET", output_field=CharField()))
    )

    reviews = (
        Review.objects.filter(user=request.user)
        .select_related("user", "ticket", "ticket__user")
        .annotate(content_type=Value("REVIEW", output_field=CharField()))
    )

    posts = sorted(
        chain(tickets, reviews),
        key=lambda p: p.time_created,
        reverse=True,
    )

    return render(request, "gestionlivre/posts.html", {"posts": posts})


User = get_user_model()


@login_required
def subscriptions(request):
    if request.method == "POST":
        form = FollowUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"].strip()
            try:
                user_to_follow = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, "Cet utilisateur n'existe pas.")
                return redirect("subscriptions")

            if user_to_follow == request.user:
                messages.error(request, "Vous ne pouvez pas vous suivre vous-même.")
                return redirect("subscriptions")

            # éviter doublon (unique_together protège aussi, mais on fait propre)
            exists = UserFollows.objects.filter(user=request.user, followed_user=user_to_follow).exists()
            if exists:
                messages.info(request, "Vous suivez déjà cet utilisateur.")
                return redirect("subscriptions")

            UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
            messages.success(request, f"Vous suivez maintenant {user_to_follow.username}.")
            return redirect("subscriptions")
    else:
        form = FollowUserForm()

    following = (
        UserFollows.objects.filter(user=request.user)
        .select_related("followed_user")
        .order_by("followed_user__username")
    )
    followers = (
        UserFollows.objects.filter(followed_user=request.user).select_related("user").order_by("user__username")
    )
    all_users = User.objects.order_by("username")

    return render(
        request,
        "gestionlivre/subscriptions.html",
        {"following": following, "followers": followers, "all_users": all_users, "form": form},
    )


@login_required
def unfollow(request, followed_user_id):
    follow = get_object_or_404(UserFollows, user=request.user, followed_user_id=followed_user_id)
    follow.delete()
    messages.success(request, "Désabonnement effectué.")
    return redirect("subscriptions")
