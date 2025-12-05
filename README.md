# Calendar generator with Python and LaTeX

A 'simple' calendar generator (PDF) with Python and LaTeX.

## Description

This project uses Python and Jinja2 to generate a LaTeX file from a template, which is then compiled to produce a PDF calendar. The calendar layout is based on the [Monthly Calendar template](https://www.latextemplates.com/template/monthly-calendar) by [LaTeXTemplates.com](https://www.latextemplates.com/).

### Technologies Used

- Programming Language: [Python 3](https://www.python.org/)
- Packages: [Jinja2](https://palletsprojects.com/projects/jinja/)
- Package Management: [Poetry](https://python-poetry.org/)
- Task Runner: [Poe the Poet](https://poethepoet.natn.io/)
- LaTeX Distribution: [TinyTeX](https://yihui.org/tinytex/)
- LaTeX Template: [Monthly Calendar template](https://www.latextemplates.com/template/monthly-calendar)
- Dev Environment: [VS Code](https://code.visualstudio.com/) with the [python-poetry-starter](https://github.com/jhordyess/python-poetry-starter) template

### Screenshot

<a href="app/generated/index.pdf"><img src="https://res.cloudinary.com/jhordyess/image/upload/v1679528092/latex/calendar-generator.png" alt="March 23'"></a>

## How to use

### Prerequisites

1. Install [Python](https://www.python.org/downloads/) (3.10+ recommended).
2. Check if [pip](https://pip.pypa.io/) is installed by running: ``python -m pip --version``, by default it comes with Python installations. If not [review the docs](https://pip.pypa.io/en/stable/installation/).
3. Install [pipx](https://pipx.pypa.io/stable/installation/), but you can use `pip` to install it:

```sh
python -m pip install --user pipx
pipx ensurepath
# Restart your terminal
```

4. Install [Poetry](https://python-poetry.org/) and [Poe the Poet](https://poethepoet.natn.io/) using `pipx`:

```sh
pipx install poetry poethepoet
```

5. (optional) Configure `Poetry` to use in-project virtual environments, which keeps the virtual environment inside the project directory:

```sh
poetry config virtualenvs.in-project true
```

6. Install [LaTeX](https://www.latex-project.org/get/) with a distribution like [TeX Live](https://www.tug.org/texlive/) or [MiKTeX](https://miktex.org/download), depending on your OS. This project was tested with [TinyTeX](https://yihui.org/tinytex/#installation) with the `extsizes` and `palatino` packages, which can be installed using `tlmgr`:

```sh
tlmgr install extsizes palatino
```

## Getting Started

1. Clone the repository:

```sh
git clone https://github.com/jhordyess/calendar-generator.git
```

2. Navigate to the project folder:

```sh
cd calendar-generator
```

3. Install dependencies:

```sh
poetry install
```

4. Generate the calendar:

```sh
poe gen-pdf
```

5. The generated PDF file will be located at [`app/generated/index.pdf`](app/generated/index.pdf).

## License

© 2022 [Jhordyess](https://github.com/jhordyess). Under the [MIT](https://choosealicense.com/licenses/mit/) license.

---

Made with 💪 by [Jhordyess](https://www.jhordyess.com/)
