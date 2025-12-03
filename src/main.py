import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
from jinja2 import Environment, FileSystemLoader

CSV_FILE = "data.csv"
JINJA_TEMPLATE = "template.tex.jinja"
TEX_TEMPLATE = "generated/index.tex"


class CalendarGenerator:
  def __init__(self, year=-1, num_months=12):
    self.year = datetime.now().year if (year == -1) else year
    self.num_months = num_months
    self.csv_data = self._read_csv(CSV_FILE)
    self.env = Environment(loader=FileSystemLoader('.'))

  def generate_calendar(self):
    template = self.env.get_template(JINJA_TEMPLATE)
    months = self._generate_months(datetime(self.year, 1, 1), self.num_months)
    return template.render(months=months)

  def _read_csv(self, csv_file):
    data = {}
    with open(csv_file, 'r') as file:
      reader = csv.reader(file)
      next(reader)  # Skip the header
      for row in reader:
        data[row[0]] = row[1]  # date is the key, title is the value
    return data

  def _generate_months(self, date, num_months):
    months = []
    for x in range(num_months):
      months.append(self._generate_month(date+relativedelta(months=x)))
    return months

  def _generate_month(self, date):
    month_name = date.strftime("%B")
    year = date.strftime("%Y")
    days_in_month = int((date + relativedelta(day=31)).strftime("%d"))
    first_emptyCount = int(date.replace(day=1).strftime("%w"))
    last_emptyCount = 6 - int(date.replace(day=days_in_month).strftime("%w"))
    days = self._generate_days(days_in_month, date.strftime("%m"), year)

    return {
        'name': month_name,
        'year': year,
        'days': [{'is_blank': True} for _ in range(first_emptyCount)] + days + [{'is_blank': True} for _ in range(last_emptyCount)]
    }

  def _generate_days(self, num_days, month, year):
    days = []
    for day in range(1, num_days + 1):
      date_key = f"{year}-{int(month):02d}-{int(day):02d}"
      content = self.csv_data.get(date_key, "")
      title = "" if content == "" else ""
      days.append({'title': title, 'content': content})
    return days


def main():
  calendar_generator = CalendarGenerator(2025)
  calendar_template = calendar_generator.generate_calendar()
  with open(TEX_TEMPLATE, "w") as file:
    file.write(calendar_template)


if __name__ == "__main__":
  main()
