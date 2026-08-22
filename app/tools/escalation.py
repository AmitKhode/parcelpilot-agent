from typing import Dict, Any
from app.data.repository import record_escalation
from app.agent.state import confirmation_manager

def propose_escalation(ticket_id: str, reason: str, urgency: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
    """Proposes a state-changing escalation and queues it for explicit human confirmation."""
    session_id = user_context.get("session_id", "default_session")
    action_payload = {
        "type": "ESCALATE_TICKET",
        "ticket_id": ticket_id,
        "reason": reason,
        "urgency": urgency,
        "user_id": user_context.get("user_id", "support_user")
    }
    confirmation_manager.set_pending(session_id, action_payload)
    return {
        "status": "WAITING_FOR_CONFIRMATION",
        "prompt": f"Ready to create this escalation for ticket {ticket_id} with urgency '{urgency}' (Reason: {reason}). Confirm?",
        "action_details": action_payload
    }

def execute_confirmed_escalation(action_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Executes the state change once confirmation is obtained."""
    result = record_escalation(
        ticket_id=action_payload["ticket_id"],
        reason=action_payload["reason"],
        urgency=action_payload["urgency"],
        created_by=action_payload["user_id"]
    )
    return {
        "status": "SUCCESS",
        "message": f"Ticket {action_payload['ticket_id']} was successfully escalated.",
        "record": result
    }