from django.urls import path

from .views import helloworld

urlpatterns = [
    path("", helloworld),
]
