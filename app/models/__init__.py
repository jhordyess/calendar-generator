from dataclasses import dataclass
from typing import List


@dataclass
class DayCell:
    is_blank: bool
    title: str = ""
    content: str = ""


@dataclass
class Month:
    name: str
    year: str
    days: List[DayCell]

__all__ = ["DayCell", "Month"]
