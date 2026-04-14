from django.urls import path
from .views import ProductListView, ShopListView, OrderListView

urlpatterns = [
    path("products/", ProductListView.as_view()),
    path("shops/", ShopListView.as_view()),
    path("orders/", OrderListView.as_view()),
]
