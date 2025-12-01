from typing import List, Dict

def mock_search_hotels(destination: str, dates: Dict) -> List[Dict]:
    return [
        {"name": "Demo Hotel", "price_per_night": 120},
        {"name": "Comfort Stay", "price_per_night": 90}
    ]
