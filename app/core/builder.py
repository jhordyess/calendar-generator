from datetime import datetime, date
import calendar
from typing import List, Dict, Optional

from app.models import DayCell, Month


class CalendarBuilder:
    """Build month and day structures for templates."""

    def __init__(self, year: Optional[int] = None, num_months: int = 12, is_sunday_start: bool = False, events: Optional[Dict[str, str]] = None) -> None:
        self.year = year if year is not None else datetime.now().year
        self.num_months = num_months
        # keep existing mapping: 0=Mon start, 1=Sunday-start switch used in original
        self.week_start_index = 0 if not is_sunday_start else 1
        self.events: Dict[str, str] = events or {}

    def generate(self) -> List[Month]:
        start_date = date(self.year, 1, 1)
        return self._generate_months(start_date, self.num_months)

    def _generate_months(self, start: date, count: int) -> List[Month]:
        months: List[Month] = []
        for i in range(count):
            year = start.year + (start.month - 1 + i) // 12
            month = ((start.month - 1 + i) % 12) + 1
            months.append(self._generate_month(year, month))
        return months

    def _generate_month(self, year: int, month: int) -> Month:
        month_name = calendar.month_name[month]
        first_weekday, days_in_month = calendar.monthrange(year, month)
        first_empty = (first_weekday + self.week_start_index) % 7
        last_weekday = datetime(year, month, days_in_month).weekday()
        last_empty = (6 - last_weekday - self.week_start_index) % 7

        days = self._generate_days(year, month, days_in_month)
        day_cells: List[DayCell] = (
            [DayCell(is_blank=True) for _ in range(first_empty)] +
            days +
            [DayCell(is_blank=True) for _ in range(last_empty)]
        )

        return Month(name=month_name, year=str(year), days=day_cells)

    def _generate_days(self, year: int, month: int, num_days: int) -> List[DayCell]:
        result: List[DayCell] = []
        for d in range(1, num_days + 1):
            key = f"{year}-{month:02d}-{d:02d}"
            content = self.events.get(key, "")
            # title = str(d)
            title = ""
            result.append(DayCell(is_blank=False, title=title, content=content))
        return result
