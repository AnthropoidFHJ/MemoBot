import json
from pathlib import Path
from typing import List, Dict, Any
import asyncio
from app.config.config import settings


DATA_FILE = Path(settings.HISTORY_FILE)


class HistoryStore:

    def __init__(self):
        self._lock: asyncio.Lock | None = None  
        self._data: Dict[str, List[Dict[str, Any]]] = {}
        self._sync_load()

    def _get_lock(self) -> asyncio.Lock:
        if self._lock is None:
            self._lock = asyncio.Lock()
        return self._lock

    def _sync_load(self) -> None:
        try:
            if DATA_FILE.exists():
                with DATA_FILE.open("r", encoding="utf-8") as f:
                    self._data = json.load(f)
        except Exception:
            self._data = {}

    async def _save(self) -> None:
        def _write(d):
            DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
            with DATA_FILE.open("w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)

        await asyncio.to_thread(_write, self._data)

    def _key(self, user_id: int, session_id: str) -> str:
        return f"{user_id}:{session_id}"

    async def get_history(self, user_id: int, session_id: str) -> List[Dict[str, Any]]:
        key = self._key(user_id, session_id)
        async with self._get_lock():
            return list(self._data.get(key, []))

    async def append_message(self, user_id: int, session_id: str, message: Dict[str, Any]) -> None:
        key = self._key(user_id, session_id)
        async with self._get_lock():
            arr = self._data.get(key, [])
            arr.append(message)
            self._data[key] = arr
            await self._save()

    async def clear_session(self, user_id: int, session_id: str) -> None:
        key = self._key(user_id, session_id)
        async with self._get_lock():
            if key in self._data:
                del self._data[key]
                await self._save()
