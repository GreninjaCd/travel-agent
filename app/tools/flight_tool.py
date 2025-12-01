from typing import List, Dict

def mock_search_flights(origin: str, destination: str, dates: Dict) -> List[Dict]:
    return [
        {"airline": "DemoAir", "price": 199, "departure": dates.get("depart")},
        {"airline": "MockWings", "price": 249, "departure": dates.get("depart")}
    ]
