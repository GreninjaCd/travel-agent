from typing import List, Dict, Any
import asyncio
from app.tools.flight_tool import mock_search_flights


class FlightAgent:
    async def search_flights_async(self, origin: str, destination: str, dates: Dict[str, Any]) -> List[Dict]:
        # The underlying tool is sync (mock); run in thread to avoid blocking
        return await asyncio.to_thread(mock_search_flights, origin, destination, dates)

    # Backwards-compatible sync wrapper
    def search_flights(self, origin: str, destination: str, dates: Dict) -> List[Dict]:
        return mock_search_flights(origin, destination, dates)
