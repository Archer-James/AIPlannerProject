import calendar
from datetime import datetime, timedelta
import reflex as rx


class GenWeeklyCal(rx.State):
    """
    Generate Weekly Calendar class

    now : datetime
        current date
    current_week_start:
        start date of the current week
    days: list
        list of days in the current week
    label: string
        Title of the calendar
    """
    now = datetime.now()
    current_week_start: datetime = now - timedelta(days=now.weekday())  # Start of the week (Monday)
    days: list[datetime] = []
    dates: list[list[str]] = []

    label = ""

    def get_week_label(self):
        """Set the label variable to a string of the week for Title of calendar"""
        week_start = self.current_week_start.strftime("%B %d, %Y")
        week_end = (self.current_week_start + timedelta(days=6)).strftime("%B %d, %Y")
        self.label = f"Week of {week_start} to {week_end}"

    def init_week(self):
        """Initialize the list of days in the current week"""
        self.days = [self.current_week_start + timedelta(days=i) for i in range(7)]
        self.get_week_label()

    def next_week(self):
        """Increment week and reinitialize calendar"""
        self.current_week_start += timedelta(weeks=1)
        self.init_week()

    def prev_week(self):
        """Decrement week and reinitialize calendar"""
        self.current_week_start -= timedelta(weeks=1)
        self.init_week()

    def make_dates(self):
        """
        Set dates list as list of numbers of days to iterate through
        """
        self.days = [self.current_week_start + timedelta(days=i) for i in range(7)]
        self.dates = [[day.strftime("%A, %B %d") for day in self.days]]  # Format dates for display
        self.get_week_label()

    def init_week(self):
        """Initialize the week by generating dates and setting the label"""
        self.make_dates()  # Populate days and dates
        self.get_week_label()