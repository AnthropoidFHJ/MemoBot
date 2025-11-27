from typing import List, Dict, Any
import httpx
from app.config.config import settings

class AIService:
    def __init__(self):
        self.api_key: str = settings.GROQ_API_KEY
        self.model: str = settings.GROQ_MODEL
    async def generate_reply(self, user_id: int, session_id: str, message: str, history: List[Dict[str, Any]]) -> str:

        if not self.api_key:
            summary = await self._summarize_history(history)
            return f"(Assistant) Summary: {summary} Your message: {message}"

        messages = [
            {"role": "system", "content": "You are helpful Personal AI Assistant."}
        ]
        for m in history:
            role = m.get("role", "user")
            content = m.get("content", "")
            messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": message})

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.4,
            "max_tokens": 800
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(url, headers=headers, json=payload)
                resp.raise_for_status()
                j = resp.json()
                choices = j.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content", str(j))
                return str(j)
        except httpx.HTTPStatusError as e:
            error_detail = ""
            try:
                error_detail = e.response.json().get("error", {}).get("message", "")
            except Exception:
                pass
            return f"(API Error: {e.response.status_code}) {error_detail or 'Could not generate reply.'}"
        except Exception as e:
            return f"(Error) {str(e)}"

    async def _summarize_history(self, history: List[Dict[str, Any]]) -> str:
        if not history:
            return "no prior messages"
        last_roles = [f"{h.get('role')}: {str(h.get('content'))[:60]}" for h in history[-3:]]
        return " | ".join(last_roles)