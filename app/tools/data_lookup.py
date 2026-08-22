from typing import Dict, Any, Optional
from app.data.loader import repo
from app.security.access_control import AuthorizationError

def get_order_details(order_id: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
    try:
        res = repo.get_order(order_id, user_context)
        if not res:
            return {"error": f"Order {order_id} not found."}
        return res
    except AuthorizationError as ae:
        return {"error": str(ae)}

def get_ticket_details(ticket_id: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
    try:
        res = repo.get_ticket(ticket_id, user_context)
        if not res:
            return {"error": f"Ticket {ticket_id} not found."}
        return res
    except AuthorizationError as ae:
        return {"error": str(ae)}

def list_customer_tickets(account_id: Optional[str], user_context: Dict[str, Any]) -> Dict[str, Any]:
    try:
        res = repo.list_tickets(account_id, user_context)
        return {"tickets": res}
    except AuthorizationError as ae:
        return {"error": str(ae)}

def list_customer_orders(account_id: Optional[str], user_context: Dict[str, Any]) -> Dict[str, Any]:
    try:
        res = repo.list_orders(account_id, user_context)
        return {"orders": res}
    except AuthorizationError as ae:
        return {"error": str(ae)}