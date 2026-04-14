from django.urls import path
from .views import RoleListView, BusinessElementListView, AccessRuleListCreateView, AccessRuleDetailView

urlpatterns = [
    path("roles/", RoleListView.as_view()),
    path("elements/", BusinessElementListView.as_view()),
    path("rules/", AccessRuleListCreateView.as_view()),
    path("rules/<int:pk>/", AccessRuleDetailView.as_view()),
]
