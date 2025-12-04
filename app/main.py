from pathlib import Path
import csv
from datetime import datetime, date
import calendar
from typing import Dict, List, Any, Optional
from jinja2 import Environment, FileSystemLoader

# Paths
BASE_DIR = Path(__file__).parent
CSV_FILE = BASE_DIR / "data.csv"
JINJA_TEMPLATE = "template.tex.jinja"
TEX_OUTPUT = BASE_DIR / "generated" / "index.tex"


class CalendarGenerator:
    """Generate data structures used by the LaTeX calendar Jinja template.

    Responsibilities:
    - load events from a CSV file (columns: `date`, `content`)
    - build a list of months where each month contains a list of day cells
      (either a blank cell or a day with `title` and `content`).
    """

    def __init__(self, year: Optional[int] = None, num_months: int = 12, is_sunday_start: bool = False) -> None:
        self.year = year if year is not None else datetime.now().year
        self.num_months = num_months
        self.week_start_index = 0 if not is_sunday_start else 1
        self.events: Dict[str, str] = self._load_events(CSV_FILE)
        self.env = Environment(loader=FileSystemLoader(str(BASE_DIR)))
        TEX_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    def generate(self) -> str:
        """Render the Jinja template and return the generated LaTeX string."""
        template = self.env.get_template(JINJA_TEMPLATE)
        start_date = date(self.year, 1, 1)
        months = self._generate_months(start_date, self.num_months)
        return template.render(months=months)

    def _load_events(self, csv_path: Path) -> Dict[str, str]:
        """Load events from CSV into a dict keyed by ISO date `YYYY-MM-DD`.

        Uses `csv.DictReader` for clarity and robustness.
        """
        events: Dict[str, str] = {}
        with csv_path.open(newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                key = (row.get("date") or "").strip()
                value = (row.get("content") or "").strip()
                if key:
                    events[key] = value
        return events

    def _generate_months(self, start: date, count: int) -> List[Dict[str, Any]]:
        """Generate `count` consecutive months starting at `start`.

        This avoids relying on relative date arithmetic and computes month/year
        using integer math so the result is deterministic and clear.
        """
        months: List[Dict[str, Any]] = []
        for i in range(count):
            # compute year and month offset from start
            year = start.year + (start.month - 1 + i) // 12
            month = ((start.month - 1 + i) % 12) + 1
            months.append(self._generate_month(year, month))
        return months

    def _generate_month(self, year: int, month: int) -> Dict[str, Any]:
        """Return a dict with `name`, `year`, and `days` for the given month.

        `days` is a list of cells where each cell is either `{'is_blank': True}`
        for padding cells, or `{'title': ..., 'content': ...}` for real days.
        """
        month_name = calendar.month_name[month]
        # first_weekday is 0=Mon..6=Sun
        first_weekday, days_in_month = calendar.monthrange(year, month)
        # Adjust first_weekday based on week_start_index
        first_empty = (first_weekday + self.week_start_index) % 7
        # last_weekday is 0=Mon..6=Sun
        last_weekday = datetime(year, month, days_in_month).weekday() 
        # Adjust last_weekday based on week_start_index
        last_empty = (6 - last_weekday - self.week_start_index) % 7

        days = self._generate_days(year, month, days_in_month)
        day_cells = (
            [{'is_blank': True} for _ in range(first_empty)] +
            days +
            [{'is_blank': True} for _ in range(last_empty)]
        )

        return {
            'name': month_name,
            'year': str(year),
            'days': day_cells,
        }

    def _generate_days(self, year: int, month: int, num_days: int) -> List[Dict[str, str]]:
        """Generate the list of day cells for a month.

        Each day cell has `title` (the day number) and `content` (event text or empty).
        """
        result: List[Dict[str, str]] = []
        for d in range(1, num_days + 1):
            key = f"{year}-{month:02d}-{d:02d}"
            content = self.events.get(key, "")
            title = "" # TODO: can use a custom title if needed
            result.append({'title': title, 'content': content})
        return result


def main() -> None:
    generator = CalendarGenerator(2025, is_sunday_start=True)
    tex = generator.generate()
    TEX_OUTPUT.write_text(tex, encoding='utf-8')


if __name__ == '__main__':
    main()
