from django.urls import path
from .views_users import MeView

urlpatterns = [
    path("me/", MeView.as_view()),
]
