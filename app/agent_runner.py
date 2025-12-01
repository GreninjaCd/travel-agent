import asyncio
from typing import Any, Optional
from app.agents.travel_agent import TravelAgent
from app.memory.session_service import SessionService
from app.memory.memory_bank import MemoryBank
from app.observability import log_info


class AgentRunner:
    """Async orchestration entrypoint for the travel agents.

    Responsibilities:
    - Run the travel agent orchestration asynchronously
    - Support session resume/save in the MemoryBank
    - Expose a simple API used by CLI and the Node server
    """

    def __init__(self):
        self.master = TravelAgent()
        self.sessions = SessionService()
        self.memory = MemoryBank()

    async def run(self, payload: dict, session_id: Optional[str] = None) -> Any:
        log_info("AgentRunner: starting run")

        # Resume state if available
        if session_id:
            prev = self.memory.load(session_id)
            if prev:
                payload = {**prev.get("last_payload", {}), **payload}

        # Delegate to master agent which implements async handle_request
        result = await self.master.handle_request(payload)

        if session_id:
            self.memory.save(session_id, {"last_result": result, "last_payload": payload})
            log_info(f"Saved result to memory for session={session_id}")

        return result
