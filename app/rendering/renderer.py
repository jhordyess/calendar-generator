from pathlib import Path
from typing import List
from jinja2 import Environment, FileSystemLoader

from app.models import Month


class Renderer:
    """Render LaTeX templates with Jinja2."""

    def __init__(self, template_dir: Path) -> None:
        self.env = Environment(loader=FileSystemLoader(str(template_dir)))

    def render(self, template_name: str, months: List[Month]) -> str:
        template = self.env.get_template(template_name)
        return template.render(months=months)
