import calendar
from datetime import datetime

import reflex as rx


class GenCalendar(rx.State):
    """
    Generate Calendar class

    now : datetime
        current date
    current_month :
        current month to start at
    current_year:
        current year to start at
    dates: list
        list of weeks of dates of the year
    label: string
        Title of the calendar
    """
    now = datetime.now()
    current_month: int = now.month
    current_year: int = now.year
    dates: list[list[str]] = []
    label = ""

    def days_in_month(self):
        """
        Function to get the number of days in a month and when the month starts

         Returns: 
         int: first weekday of the month
         int: number of days in the month
         
         
        """
        cal = calendar.Calendar(firstweekday=6)  # Start the week on Sunday
        return calendar.monthrange(self.current_year, self.current_month)

    def get_month_year_label(self):
        """Function to set the label variable to a string of the month and year for Title of calendar"""
        month_name = calendar.month_name[self.current_month]
        month_year_string = str(month_name + " " + str(self.current_year))
        self.label = month_year_string

    def next_month(self):
        """Function to increment month and reinitialize calendar"""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.init_calendar()

    def prev_month(self):
        """Function to decrement month and reinitialize calendar"""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.init_calendar()

    def make_dates(self):
        """Function to set dates list as list of numbers of days to iterate through"""
        self.dates = []
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
            week.extend([0] * (7 - len(week)))
            self.dates.append(week)

    def init_calendar(self):
        """Function that runs the initialization of variables"""
        self.make_dates()
        self.get_month_year_label()
