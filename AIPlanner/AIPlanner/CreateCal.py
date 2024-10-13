import reflex as rx
import calendar
from datetime import datetime


class GenCalendar(rx.State):
    # Define reactive state variables for month and year
    now = datetime.now()
    current_month: int = now.month
    current_year: int = now.year
    dates: list[list[str]] = []

    def days_in_month(self):
        """Get the list of weeks for the current month, where each week is a list of days."""
        cal = calendar.Calendar(firstweekday=6)  # Start the week on Sunday
        return calendar.monthrange(self.current_year, self.current_month)

    def get_month_year_label(self):
        """Return a string of the current month and year."""
        month_name = calendar.month_name[self.current_month]
        month_year_string = str(month_name + " "+self.current_year)
        return  month_year_string

    def next_month(self):
        """Move to the next month."""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1

    def prev_month(self):
        """Move to the previous month."""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1

    
    def make_dates(self):

        first_day, days = self.days_in_month()
        days_in_month = [datetime(self.current_year, self.current_month, day) 
                             for day in range(1, days + 1)]
        week = [0] * first_day
        for day in days_in_month:
            week.append(day.day)
            if len(week) == 7:
                self.dates.append(week)
                week = []
        if week:
            week.extend([0]*(7-len(week)))
            self.dates.append(week)

    def init_calendar(self):
        self.make_dates()