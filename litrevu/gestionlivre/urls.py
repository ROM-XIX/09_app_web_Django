# litrevu/gestionlivre/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("tickets/create/", views.ticket_create, name="ticket_create"),
    path("tickets/<int:ticket_id>/review/", views.review_create_for_ticket, name="review_create_for_ticket"),
    path("reviews/create/", views.ticket_and_review_create, name="ticket_and_review_create"),
]
