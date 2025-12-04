from pathlib import Path
from typing import Optional

from app.core.events import load_events
from app.core.builder import CalendarBuilder
from app.rendering.renderer import Renderer

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "data.csv"
TEMPLATE_NAME = "template.tex.jinja"
TEX_OUTPUT = BASE_DIR / "generated" / "index.tex"

def main(year: Optional[int] = None, num_months: int = 12, is_sunday_start: bool = False, csv_path: Optional[Path] = None, template_name: Optional[str] = None, out_path: Optional[Path] = None) -> str:
    csv_path = csv_path or CSV_FILE
    template_name = template_name or TEMPLATE_NAME
    out_path = out_path or TEX_OUTPUT

    events = load_events(csv_path)

    builder = CalendarBuilder(year=year, num_months=num_months, is_sunday_start=is_sunday_start, events=events)
    months = builder.generate()
    
    renderer = Renderer(BASE_DIR)
    tex = renderer.render(template_name, months)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(tex, encoding='utf-8')
    return tex


if __name__ == '__main__':
    main(year=2025, is_sunday_start=True)