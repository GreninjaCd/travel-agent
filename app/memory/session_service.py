from typing import Dict

class SessionService:
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}

    def get(self, session_id: str) -> Dict:
        return self.sessions.get(session_id, {})

    def set(self, session_id: str, data: Dict):
        self.sessions[session_id] = data
