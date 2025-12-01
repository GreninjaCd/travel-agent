import os
import asyncio
from typing import Any, Dict


class LLMAgent:
    """LLM adapter. When `OPENAI_API_KEY` is set this will call OpenAI's Chat Completions API
    using the modern `openai` client (OpenAI.ChatCompletions). Falls back to a deterministic
    template when the key is not available or the call fails.
    """

    def __init__(self):
        self._key = os.environ.get("OPENAI_API_KEY")
        self._model = os.environ.get("LLM_MODEL", "gpt-3.5-turbo")
        self._client = None
        if self._key:
            try:
                # modern client
                from openai import OpenAI

                self._client = OpenAI(api_key=self._key)
            except Exception:
                # If import or init fails, we'll fallback to local summary
                self._client = None

    async def summarize_itinerary(self, data: Dict[str, Any]) -> str:
        if self._client:
            try:
                return await asyncio.to_thread(self._call_openai, data)
            except Exception as e:
                return self._local_summary(data) + f"\n\n(Note: OpenAI call failed: {e})"

        return self._local_summary(data)

    def _call_openai(self, data: Dict[str, Any]) -> str:
        # Build messages for chat completion
        flights = data.get("flights", [])
        hotels = data.get("hotels", [])
        activities = data.get("activities", [])

        system = "You are an assistant that creates short, actionable travel itineraries for users."
        user = (
            "Create a concise itinerary summary for the following JSON data. Include top flight, hotel, "
            "a suggested activity list, and one-sentence rationale for why the chosen options fit the user.\n\n"
            f"Data:\n{data}"
        )

        # Using the new client interface
        resp = self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            max_tokens=120,
            temperature=0.7,
        )

        # response shape: resp.choices[0].message.content
        choices = getattr(resp, "choices", None) or []
        if choices:
            first = choices[0]
            # New SDK may store message as dict or object
            msg = None
            if isinstance(first, dict):
                msg = first.get("message", {}).get("content") or first.get("text")
            else:
                # object with attributes
                msg = getattr(getattr(first, "message", {}), "content", None) or getattr(first, "text", None)

            if msg:
                return str(msg).strip()

        return self._local_summary(data)

    def _local_summary(self, data: Dict[str, Any]) -> str:
        flights = data.get("flights", [])
        hotels = data.get("hotels", [])
        activities = data.get("activities", [])

        summary_lines = ["Trip summary:"]
        if flights:
            f = flights[0]
            summary_lines.append(f"Flight: {f.get('airline')} at ${f.get('price')}")
        if hotels:
            h = hotels[0]
            summary_lines.append(f"Hotel: {h.get('name')} at ${h.get('price_per_night')}/night")
        if activities:
            summary_lines.append(f"Activities: {', '.join(a['name'] for a in activities[:3])}")

        summary_lines.append("(This summary was generated locally because OpenAI isn't configured.)")
        return "\n".join(summary_lines)
