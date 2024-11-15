import calendar
from datetime import datetime, timedelta
import reflex as rx


class GenWeeklyCal(rx.State):
    """
    Generate Weekly Calendar class

    now(datetime): current date
    current_year(int): current year
    current_week_start(datetime): start date of the current week
    days(list): list of days in the current week
    dates(list[list[str]]): nested list of days in week
    current_month(int): current month
    week_number(int): number of week
    label(string): Title of the calendar
    """
    now = datetime.now()
    current_year: int = now.year
    current_week_start: datetime = now - timedelta(days=now.weekday())  # Start of the week (Monday)
    days: list[datetime] = []
    dates: list[list[str]] = []
    current_month: int = now.month
    week_number = now.isocalendar().week
    label = ""

    def init_week(self):
        """Initialize the list of days in the current week"""
        self.make_dates()  # Generate dates for the week
        self.get_week_label()

    def get_week_label(self):
        """Set the label variable to a string of the week for Title of calendar"""
        month_name = calendar.month_name[self.current_month]
        self.label = "Week of "+ month_name + " "+str(self.current_week_start.day)


    def next_month(self):
        """increment month and reinitialize calendar"""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1

    def prev_month(self):
        """Decrement month and reinitialize calendar"""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1

    def next_week(self):
        """Increment week and reinitialize calendar"""
        self.current_week_start += timedelta(weeks=1)
        if self.week_number == 4:
            self.week_number = 1
            self.next_month()
        else:
            self.week_number += 1
        self.init_week()

    def prev_week(self):
        """Decrement week and reinitialize calendar"""
        self.current_week_start -= timedelta(weeks=1)
        if self.week_number == 1:
            self.week_number = 4
            self.prev_month()
        else:
            self.week_number -= 1
        self.init_week()

    def make_dates(self):
        """Set dates list as list of numbers of days to iterate through"""
        self.days = [self.current_week_start + timedelta(days=i) for i in range(7)]
        self.dates = [[day.strftime(" %d") for day in self.days]]  # Format dates for display
        self.get_week_label()
