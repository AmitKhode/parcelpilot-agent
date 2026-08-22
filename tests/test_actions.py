from app.agent.state import confirmation_manager
from app.tools.escalation import propose_escalation, execute_confirmed_escalation

def test_escalation_confirmation_workflow():
    session_id = "test_sess_01"
    user_context = {"session_id": session_id, "user_id": "tester", "role": "SUPPORT_AGENT"}
    
    # 1. Propose action
    res = propose_escalation("TKT-501", "Production outage HTTP 500", "Critical", user_context)
    assert res["status"] == "WAITING_FOR_CONFIRMATION"
    assert confirmation_manager.get_pending(session_id) is not None
    
    # 2. Execute action after confirmed
    action = confirmation_manager.get_pending(session_id)
    exec_res = execute_confirmed_escalation(action)
    assert exec_res["status"] == "SUCCESS"
    assert exec_res["record"]["ticket_id"] == "TKT-501"