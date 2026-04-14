from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.decorators import login_required
from apps.access.permissions import has_permission

MOCK_PRODUCTS = [
    {"id": 1, "name": "Laptop Pro 15", "price": 1299.99, "owner_id": 2},
    {"id": 2, "name": "Wireless Mouse", "price": 29.99, "owner_id": 3},
    {"id": 3, "name": "USB-C Hub", "price": 49.99, "owner_id": 2},
]

MOCK_SHOPS = [
    {"id": 1, "name": "Tech World", "city": "Yerevan", "owner_id": 2},
    {"id": 2, "name": "Gadget Zone", "city": "Moscow", "owner_id": 3},
]

MOCK_ORDERS = [
    {"id": 1, "product_id": 1, "quantity": 2, "status": "delivered", "owner_id": 2},
    {"id": 2, "product_id": 3, "quantity": 1, "status": "pending",   "owner_id": 3},
    {"id": 3, "product_id": 2, "quantity": 5, "status": "shipped",   "owner_id": 2},
]


def _filter_own(items, user_id):
    return [i for i in items if i.get("owner_id") == user_id]


class ProductListView(APIView):
    def get(self, request):
        if not getattr(request, "user", None):
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        if has_permission(request.user, "products", "read_all"):
            return Response(MOCK_PRODUCTS)
        if has_permission(request.user, "products", "read"):
            return Response(_filter_own(MOCK_PRODUCTS, request.user.id))
        return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)


class ShopListView(APIView):
    def get(self, request):
        if not getattr(request, "user", None):
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        if has_permission(request.user, "shops", "read_all"):
            return Response(MOCK_SHOPS)
        if has_permission(request.user, "shops", "read"):
            return Response(_filter_own(MOCK_SHOPS, request.user.id))
        return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)


class OrderListView(APIView):
    def get(self, request):
        if not getattr(request, "user", None):
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        if has_permission(request.user, "orders", "read_all"):
            return Response(MOCK_ORDERS)
        if has_permission(request.user, "orders", "read"):
            return Response(_filter_own(MOCK_ORDERS, request.user.id))
        return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
