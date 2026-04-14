from .models import AccessRoleRule


def get_rule(user, element_name: str):
    if not user or not getattr(user, "role", None):
        return None
    try:
        return AccessRoleRule.objects.select_related("role", "element").get(
            role=user.role, element__name=element_name
        )
    except AccessRoleRule.DoesNotExist:
        return None


def has_permission(user, element_name: str, action: str) -> bool:
    rule = get_rule(user, element_name)
    if rule is None:
        return False
    return getattr(rule, f"{action}_permission", False)
