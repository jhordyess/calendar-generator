from datetime import datetime
from dateutil.relativedelta import relativedelta


class CalendarGenerator:
  def __init__(self, num_months=1, start_day=1):
    self.num_months = num_months
    self.start_day = start_day
    self.current_date = datetime.now() + relativedelta(months=-1)

  def generate_calendar(self):
    calendar_template = self._build_template()
    return calendar_template

  def _build_template(self):
    template = "\\documentclass[landscape,letterpaper]{article}\n"
    template += "\\usepackage{calendar}\n"
    template += "\\usepackage[landscape,margin=1cm]{geometry}\n"
    template += "\\begin{document}\n"
    template += "\\pagestyle{empty}"
    template += "\\noindent"
    template += "\\StartingDayNumber={0}\n".format(
        str(self.start_day) if (self.start_day >
                                0 and self.start_day < 8) else "1"
    )
    template += self._generate_months(self.current_date, self.num_months)
    template += "\\end{document}"
    return template

  def _generate_months(self, date, num_months):
    date = date + relativedelta(months=+1)
    return (
        self._generate_month(date)
        if (num_months == 1)
        else f"{self._generate_month(date)}\\pagebreak\n{self._generate_months(date, num_months-1)}"
    )

  def _generate_month(self, date):
    month_name = date.strftime("%B")
    month_number = date.strftime("%m")
    year = date.strftime("%Y")
    days_in_month = int((date + relativedelta(day=31)).strftime("%d"))
    date = date.replace(day=1)
    first_empty = int(date.strftime("%w"))
    date = date.replace(day=days_in_month)
    last_empty = 8 - int(date.strftime("%w"))
    month_template = self._build_month_template(
        month_name, year, days_in_month, first_empty, last_empty, month_number
    )
    return month_template

  def _build_month_template(
      self, month_name, year, days_in_month, first_empty, last_empty, month_number
  ):
    month_template = "\\begin{center}\n"
    month_template += f"\t\\textsc{{\\LARGE {month_name}}}\\\\\n"
    month_template += f"\t\\textsc{{\\large {year}}}\n"
    month_template += "\\end{center}\n"
    month_template += "\\begin{calendar}{.97\\textwidth}\n"
    month_template += (
        "\t"
        + self._generate_empty_days(first_empty)
        + "\\setcounter{calendardate}{1}\n"
    )
    month_template += self._generate_days(days_in_month, month_number, year)
    month_template += (
        "\t" + self._generate_empty_days(last_empty) + "\\finishCalendar\n"
    )
    month_template += "\\end{calendar}\n"
    return month_template

  def _generate_days(self, num_days=30, month=1, year=2020, day=1):
    return (
        ""
        if (day > num_days)
        else self._generate_day() + self._generate_days(num_days, month, year, day+1)
    )

  def _generate_day(self, title="", msg="\\vspace{2cm}"):
    return f"\t\\day{{{title}}}{{{msg}}}\n"

  def _generate_empty_days(self, num_empty_days=0):
    return (
        ""
        if (num_empty_days < 1)
        else f"\\BlankDay{self._generate_empty_days(num_empty_days-1)}"
    )


def main():
  calendar_generator = CalendarGenerator(12)
  calendar_template = calendar_generator.generate_calendar()
  with open("index.tex", "w") as file:
    file.write(calendar_template)


if __name__ == "__main__":
  main()
