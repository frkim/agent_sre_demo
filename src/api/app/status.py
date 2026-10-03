"""Status tracking helpers for the Contoso Trek API."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

ERROR_WINDOW = timedelta(minutes=3)


@dataclass
class ErrorWindow:
    """Tracks recent HTTP 500 responses in memory for the demo status endpoint."""

    timestamps: deque[datetime] = field(default_factory=deque)

    def record(self, when: datetime | None = None) -> None:
        current = when or datetime.now(UTC)
        self.timestamps.append(current)
        self._trim(current)

    def recent_count(self, when: datetime | None = None) -> int:
        current = when or datetime.now(UTC)
        self._trim(current)
        return len(self.timestamps)

    def _trim(self, current: datetime) -> None:
        cutoff = current - ERROR_WINDOW
        while self.timestamps and self.timestamps[0] < cutoff:
            self.timestamps.popleft()
