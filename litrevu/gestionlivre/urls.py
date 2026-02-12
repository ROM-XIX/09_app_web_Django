# litrevu/gestionlivre/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_redirect),
    path("flux/", views.feed, name="feed"),
    path("posts/", views.posts, name="posts"),
    path("abonnements/", views.subscriptions, name="subscriptions"),
    path("abonnements/<int:followed_user_id>/desabonner/", views.unfollow, name="unfollow"),
    path("tickets/create/", views.ticket_create, name="ticket_create"),
    path("tickets/<int:ticket_id>/modifier/", views.ticket_update, name="ticket_update"),
    path("tickets/<int:ticket_id>/supprimer/", views.ticket_delete, name="ticket_delete"),
    path("tickets/<int:ticket_id>/review/", views.review_create_for_ticket, name="review_create_for_ticket"),
    path("reviews/create/", views.ticket_and_review_create, name="ticket_and_review_create"),
    path("reviews/<int:review_id>/modifier/", views.review_update, name="review_update"),
    path("reviews/<int:review_id>/supprimer/", views.review_delete, name="review_delete"),
]
