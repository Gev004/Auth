from django.core.management.base import BaseCommand
from apps.access.models import Role, BusinessElement, AccessRoleRule
from apps.users.models import User
from apps.users.password_utils import hash_password


ROLES = [
    {"name": "admin",   "description": "Full access to all resources and rules management"},
    {"name": "manager", "description": "CRUD on products/shops/orders, read users"},
    {"name": "user",    "description": "CRUD own objects, read public resources"},
    {"name": "guest",   "description": "Read-only access to products and shops"},
]

ELEMENTS = [
    {"name": "users",        "description": "User accounts"},
    {"name": "products",     "description": "Product catalogue"},
    {"name": "shops",        "description": "Shop listings"},
    {"name": "orders",       "description": "Customer orders"},
    {"name": "access_rules", "description": "RBAC rules management"},
]

# (role_name, element_name, read, read_all, create, update, update_all, delete, delete_all)
RULES = [
    # admin — full access to everything
    ("admin", "users",        True,  True,  True,  True,  True,  True,  True),
    ("admin", "products",     True,  True,  True,  True,  True,  True,  True),
    ("admin", "shops",        True,  True,  True,  True,  True,  True,  True),
    ("admin", "orders",       True,  True,  True,  True,  True,  True,  True),
    ("admin", "access_rules", True,  True,  True,  True,  True,  True,  True),

    # manager — read all users; full CRUD on products/shops/orders (all)
    ("manager", "users",        True,  True,  False, False, False, False, False),
    ("manager", "products",     True,  True,  True,  True,  True,  True,  True),
    ("manager", "shops",        True,  True,  True,  True,  True,  True,  True),
    ("manager", "orders",       True,  True,  True,  True,  True,  True,  True),
    ("manager", "access_rules", False, False, False, False, False, False, False),

    # user — own objects only
    ("user", "users",        True,  False, False, True,  False, True,  False),
    ("user", "products",     True,  False, True,  True,  False, True,  False),
    ("user", "shops",        True,  False, True,  True,  False, True,  False),
    ("user", "orders",       True,  False, True,  True,  False, True,  False),
    ("user", "access_rules", False, False, False, False, False, False, False),

    # guest — read-only products and shops
    ("guest", "users",        False, False, False, False, False, False, False),
    ("guest", "products",     False, True,  False, False, False, False, False),
    ("guest", "shops",        False, True,  False, False, False, False, False),
    ("guest", "orders",       False, False, False, False, False, False, False),
    ("guest", "access_rules", False, False, False, False, False, False, False),
]

DEMO_USERS = [
    {
        "first_name": "Alice",   "last_name": "Admin",   "middle_name": "",
        "email": "admin@example.com", "password": "admin123", "role": "admin",
    },
    {
        "first_name": "Mark",    "last_name": "Manager", "middle_name": "",
        "email": "manager@example.com", "password": "manager123", "role": "manager",
    },
    {
        "first_name": "John",    "last_name": "Doe",     "middle_name": "A.",
        "email": "user@example.com", "password": "user1234", "role": "user",
    },
    {
        "first_name": "Guest",   "last_name": "User",    "middle_name": "",
        "email": "guest@example.com", "password": "guest123", "role": "guest",
    },
]


class Command(BaseCommand):
    help = "Seed initial roles, business elements, access rules and demo users"

    def handle(self, *args, **options):
        self.stdout.write("Seeding roles...")
        role_map = {}
        for r in ROLES:
            obj, created = Role.objects.get_or_create(name=r["name"], defaults={"description": r["description"]})
            role_map[obj.name] = obj
            self.stdout.write(f"  {'Created' if created else 'Exists'}: {obj.name}")

        self.stdout.write("Seeding business elements...")
        element_map = {}
        for e in ELEMENTS:
            obj, created = BusinessElement.objects.get_or_create(name=e["name"], defaults={"description": e["description"]})
            element_map[obj.name] = obj
            self.stdout.write(f"  {'Created' if created else 'Exists'}: {obj.name}")

        self.stdout.write("Seeding access rules...")
        for role_name, elem_name, read, read_all, create, update, update_all, delete, delete_all in RULES:
            obj, created = AccessRoleRule.objects.update_or_create(
                role=role_map[role_name],
                element=element_map[elem_name],
                defaults={
                    "read_permission": read,
                    "read_all_permission": read_all,
                    "create_permission": create,
                    "update_permission": update,
                    "update_all_permission": update_all,
                    "delete_permission": delete,
                    "delete_all_permission": delete_all,
                },
            )
            self.stdout.write(f"  {'Created' if created else 'Updated'}: {role_name} → {elem_name}")

        self.stdout.write("Seeding demo users...")
        for u in DEMO_USERS:
            if not User.objects.filter(email=u["email"]).exists():
                User.objects.create(
                    first_name=u["first_name"],
                    last_name=u["last_name"],
                    middle_name=u["middle_name"],
                    email=u["email"],
                    password_hash=hash_password(u["password"]),
                    role=role_map[u["role"]],
                )
                self.stdout.write(f"  Created: {u['email']} ({u['role']})")
            else:
                self.stdout.write(f"  Exists:  {u['email']}")

        self.stdout.write(self.style.SUCCESS("\nSeed complete!"))
        self.stdout.write("\nDemo credentials:")
        for u in DEMO_USERS:
            self.stdout.write(f"  {u['role']:8s}  {u['email']}  /  {u['password']}")
