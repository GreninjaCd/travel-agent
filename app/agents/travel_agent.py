import asyncio
from typing import Dict, Any
from app.agents.flight_agent import FlightAgent
from app.agents.hotel_agent import HotelAgent
from app.agents.activities_agent import ActivitiesAgent
from app.agents.llm_agent import LLMAgent
from app.observability import log_info


class TravelAgent:
    def __init__(self):
        self.flight_agent = FlightAgent()
        self.hotel_agent = HotelAgent()
        self.activities_agent = ActivitiesAgent()
        self.llm = LLMAgent()

    async def handle_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Asynchronously run child agents. Demonstrates parallel agents, LLM summarization,
        sessions & memory usage, and a basic evaluator.
        """
        origin = payload.get("origin")
        destination = payload.get("destination")
        dates = payload.get("dates", {})
        preferences = payload.get("preferences", {})

        log_info("TravelAgent: launching child agents in parallel")

        # Run flight + hotel + activities in parallel
        flights_task = asyncio.create_task(self.flight_agent.search_flights_async(origin, destination, dates))
        hotels_task = asyncio.create_task(self.hotel_agent.search_hotels_async(destination, dates))
        activities_task = asyncio.create_task(self.activities_agent.suggest_activities_async(destination))

        flights, hotels, activities = await asyncio.gather(flights_task, hotels_task, activities_task)

        # Simple evaluation: choose top flight & hotel by price + preferences
        evaluation = self.evaluate_options(flights, hotels, preferences)

        # Use LLM to create a human-friendly itinerary summary (mock/OpenAI)
        summary = await self.llm.summarize_itinerary({"flights": flights, "hotels": hotels, "activities": activities, "evaluation": evaluation})

        return {"flights": flights, "hotels": hotels, "activities": activities, "evaluation": evaluation, "summary": summary}

    def evaluate_options(self, flights, hotels, preferences):
        """Very small evaluator: score options and return best picks."""
        score = {"best_flight": None, "best_hotel": None}
        if flights:
            best = min(flights, key=lambda f: f.get("price", float("inf")))
            score["best_flight"] = best
        if hotels:
            best = min(hotels, key=lambda h: h.get("price_per_night", float("inf")))
            score["best_hotel"] = best
        return score
