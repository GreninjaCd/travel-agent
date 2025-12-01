from typing import List, Dict, Any
import asyncio


class ActivitiesAgent:
    async def suggest_activities_async(self, destination: str) -> List[Dict]:
        # simple async wrapper — in real life this could call web tools
        return await asyncio.to_thread(self._suggest_sync, destination)

    def _suggest_sync(self, destination: str) -> List[Dict]:
        return [
            {"name": "City walking tour", "duration": "3h"},
            {"name": "Museum visit", "duration": "2h"}
        ]

    def suggest_activities(self, destination: str) -> List[Dict]:
        return self._suggest_sync(destination)
