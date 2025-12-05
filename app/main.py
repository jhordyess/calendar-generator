from pathlib import Path
from typing import Optional
import argparse

from app.core.events import load_events
from app.core.builder import CalendarBuilder
from app.rendering.renderer import Renderer
from app.compiler.latex import compile_with_latexmk

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "data.csv"
TEMPLATE_NAME = "template.tex.jinja"
TEX_OUTPUT = BASE_DIR / "generated" / "index.tex"

def main(year: Optional[int] = None, num_months: int = 12, is_monday_start: bool = False, csv_path: Optional[Path] = None, template_name: Optional[str] = None, out_path: Optional[Path] = None, compile_pdf: bool = False) -> None:
    csv_path = csv_path or CSV_FILE
    template_name = template_name or TEMPLATE_NAME
    out_path = out_path or TEX_OUTPUT

    events = load_events(csv_path)

    builder = CalendarBuilder(year=year, num_months=num_months, is_sunday_start=is_monday_start, events=events)
    months = builder.generate()
    
    renderer = Renderer(BASE_DIR)
    tex = renderer.render(template_name, months)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(tex, encoding='utf-8')
    
    if compile_pdf:
        compile_with_latexmk(out_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--compile-pdf", action="store_true")
    parser.add_argument("--year", type=int, default=None)
    parser.add_argument("--num-months", type=int, default=12)
    parser.add_argument("--monday-start", action="store_true")
    
    args = parser.parse_args()
    main(year=args.year, num_months=args.num_months, is_monday_start=args.monday_start, compile_pdf=args.compile_pdf)