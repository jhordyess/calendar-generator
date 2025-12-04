from pathlib import Path
import csv
from typing import Dict


def load_events(csv_path: Path) -> Dict[str, str]:
    """Load events from CSV into a dict keyed by ISO date `YYYY-MM-DD`."""
    
    events: Dict[str, str] = {}
    with csv_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            key = (row.get("date") or "").strip()
            value = (row.get("content") or "").strip()
            if key:
                events[key] = value
    return events
