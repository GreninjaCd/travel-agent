from typing import List, Dict, Any
import asyncio
from app.tools.hotel_tool import mock_search_hotels


class HotelAgent:
    async def search_hotels_async(self, destination: str, dates: Dict[str, Any]) -> List[Dict]:
        return await asyncio.to_thread(mock_search_hotels, destination, dates)

    def search_hotels(self, destination: str, dates: Dict) -> List[Dict]:
        return mock_search_hotels(destination, dates)
