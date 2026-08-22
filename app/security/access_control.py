from enum import Enum
from typing import Optional, Dict, Any

class Role(str, Enum):
    CUSTOMER = "CUSTOMER"
    SUPPORT_AGENT = "SUPPORT_AGENT"
    ADMIN = "ADMIN"

class AuthorizationError(Exception):
    pass

def authorize(
    user_context: Dict[str, Any],
    resource_account_id: Optional[str] = None,
    action: str = "read"
) -> bool:
    """
    Enforces authorization at the data/tool layer.
    """
    role = user_context.get("role")
    user_account_id = user_context.get("account_id")

    if not role:
        raise AuthorizationError("Authentication required: Missing user role.")

    # Support agents and Admins have broad visibility
    if role in [Role.SUPPORT_AGENT.value, Role.ADMIN.value]:
        return True

    # Customer roles are strictly locked down to their assigned account
    if role == Role.CUSTOMER.value:
        if not resource_account_id:
            return True
        if user_account_id and user_account_id == resource_account_id:
            return True
        raise AuthorizationError(
            f"Access Denied: Customer '{user_account_id}' cannot access records belonging to '{resource_account_id}'."
        )

    raise AuthorizationError(f"Access Denied: Unrecognized role '{role}'.")