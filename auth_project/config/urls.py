from django.urls import path, include

urlpatterns = [
    path("api/auth/", include("apps.users.urls_auth")),
    path("api/users/", include("apps.users.urls_users")),
    path("api/admin/", include("apps.access.urls")),
    path("api/mock/", include("apps.mock_business.urls")),
]
