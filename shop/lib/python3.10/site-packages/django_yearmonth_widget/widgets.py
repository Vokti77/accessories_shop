from django.forms.widgets import Input
from django.utils import timezone
import re

YEAR_LOADS = "(?P<year>\d{4})"
MONTH_LOADS = "(?P<month>\d{1,2})"
DAY_LOADS = "(?P<day>\d{1,2})"
YEAR_MONTH_LOADS = "-".join([YEAR_LOADS, MONTH_LOADS])
YEAR_MONTH_DAY_LOADS = "-".join([YEAR_LOADS, MONTH_LOADS, DAY_LOADS])

YEAR_DUMPS = "%(year)04d"
MONTH_DUMPS = "%(month)02d"
DAY_DUMPS = "%(day)02d"
YEAR_MONTH_DUMPS = "-".join([YEAR_DUMPS, MONTH_DUMPS])
YEAR_MONTH_DAY_DUMPS = "-".join([YEAR_DUMPS, MONTH_DUMPS, DAY_DUMPS])

class DjangoYearMonthWidget(Input):
    input_type = "text"
    template_name = "django-yearmonth-widget/django-yearmonth-widget.html"

    class Media:
        js = [
            "jquery3/jquery.js",
            "django-yearmonth-widget/js/sprintf.min.js",
            "django-yearmonth-widget/js/django-yearmonth-widget.js",
        ]

    def __init__(self, attrs=None, value_dumps=None, value_loads=None, years=None, start_year=None, end_year=None, prev_years=10, next_years=0, day_value=1):
        self.day_value = day_value
        self.value_dumps = value_dumps or YEAR_MONTH_DAY_DUMPS
        self.value_loads = value_loads
        if years:
            self.years = years
        else:
            now = timezone.now()
            start_year = start_year or now.year - prev_years
            end_year = end_year or now.year + next_years
            self.years = list(range(start_year, end_year + 1))
        attrs = attrs or {}
        attrs["data-value-dumps"] = self.value_dumps
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        if not value:
            value_info = {
                "value": "",
                "year": "",
                "month": "",
                "day": "",
            }
        elif isinstance(value, str):
            try:
                info = re.match(YEAR_MONTH_LOADS, value).groupdict()
                value_info = {
                    "value": value,
                    "year": int(info.get("year", 0)),
                    "month": int(info.get("month", 0)),
                    "day": int(info.get("day", 0)),
                }
            except:
                value_info = {
                    "value": value,
                    "year": 0,
                    "month": 0,
                    "day": 0,
                }
        else:
            value_info = {
                "year": value.year,
                "month": value.month,
                "day": value.day,
            }
            value = self.value_dumps % value_info
            value_info["value"] = value
        attrs = attrs or {}
        attrs["class"] = attrs.get("class", "") + " django-yearmonth-widget-input"
        attrs["data-day-value"] = self.day_value
        attrs["hidden"] = "hidden"
        context = super().get_context(name, value, attrs)
        context["years"] = self.years
        context["months"] = list(range(1, 13))
        context["value_info"] = value_info
        return context
