from datetime import datetime
from dateutil.relativedelta import relativedelta


def template(n_months=1, ini_day=1):
    date = datetime.now() + relativedelta(months=-1)
    out = ""
    out += "\\documentclass[landscape,letterpaper]{article}\n"
    out += "\\usepackage{calendar}\n"
    out += "\\usepackage[landscape,margin=1cm]{geometry}\n"
    out += "\\begin{document}\n"
    out += "\\pagestyle{empty}"
    out += "\\noindent"
    out += "\\StartingDayNumber={0}\n".format(
        str(ini_day) if (ini_day > 0 and ini_day < 8) else "1"
    )
    out += n_month(date, n_months)
    out += "\\end{document}"
    return out


def n_month(date, nmeses):
    date = date + relativedelta(months=+1)
    return (
        month(date)
        if (nmeses == 1)
        else f"{month(date)}\\pagebreak\n{n_month(date, nmeses-1)}"
    )


def month(date):
    _month = date.strftime("%B")
    _year = date.strftime("%Y")
    days_in_month = int((date + relativedelta(day=31)).strftime("%d"))
    #
    date = date.replace(day=1)
    fst_empty = int(date.strftime("%w"))
    #
    date = date.replace(day=days_in_month)
    lst_empty = 8 - int(date.strftime("%w"))
    #
    out = ""
    out += "\\begin{center}\n"
    out += f"\t\\textsc{{\\LARGE {_month}}}\\\\\n"
    out += f"\t\\textsc{{\\large {_year}}}\n"
    out += "\\end{center}\n"
    out += "\\begin{calendar}{.97\\textwidth}\n"
    out += "\t" + empty(fst_empty) + "\\setcounter{calendardate}{1}\n"
    out += n_day(days_in_month)
    out += "\t" + empty(lst_empty) + "\\finishCalendar\n"
    out += "\\end{calendar}\n"
    return out


def n_day(cnt=30):
    return "" if (cnt < 1) else day() + n_day(cnt - 1)


def day(title="", msg="\\vspace{2cm}"):
    return f"\t\\day{{{title}}}{{{msg}}}\n"


def empty(cnt=0):
    return "" if (cnt < 1) else f"\\BlankDay{empty(cnt-1)}"


f = open("index.tex", "w")
f.write(template(12))
f.close()
