from typing import Dict, Any, Optional

class ConfirmationManager:
    """Manages multi-turn state-changing confirmations."""
    def __init__(self):
        self._pending_actions: Dict[str, Dict[str, Any]] = {}

    def set_pending(self, session_id: str, action: Dict[str, Any]):
        self._pending_actions[session_id] = action

    def get_pending(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self._pending_actions.get(session_id)

    def clear(self, session_id: str):
        if session_id in self._pending_actions:
            del self._pending_actions[session_id]

confirmation_manager = ConfirmationManager()