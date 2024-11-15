from datetime import date, timedelta

class RecurFrequency:
    """
    Class for managing recurring task frequencies.

    Attributes:
    DAILY (str): Constant representing daily recurrence.
    WEEKLY (str): Constant representing weekly recurrence.
    MONTHLY (str): Constant representing monthly recurrence.
    DAY_NAMES (list): List of abbreviated day names for weekly tasks.
    """

    # Recurring options
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"

    # List of days of the week
    DAY_NAMES = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    def __init__(self, frequency, end_date=None, days_of_week=None):
<<<<<<< HEAD
        """Initialization function."""
=======
        """
        Initializes a new instance of the RecurFrequency class.

        Parameters:
        frequency (str): The recurrence frequency ('DAILY', 'WEEKLY', or 'MONTHLY').
        end_date (date, optional): The end date of the recurrence. Defaults to None.
        days_of_week (list, optional): List of days (0-6, where 0 is Sunday) for weekly recurrence. Defaults to None.

        Raises:
        ValueError: If the frequency is invalid.
        """
>>>>>>> 21a72f62f97f3a87945109bc740b077be221c049
        if frequency not in [self.DAILY, self.WEEKLY, self.MONTHLY]:
            raise ValueError("Invalid frequency")
        self.frequency = frequency
        self.end_date = end_date
        self.days_of_week = days_of_week

    def get_next_occurrence(self, start_date):
        """
        Gets the next occurrence of a recurring task based on the frequency.

        Parameters:
        start_date (date): The starting date for calculating the next occurrence.

        Returns:
        date: The next occurrence date, or None if there are no further occurrences.
        """
        if self.end_date and start_date > self.end_date:
            return None

        if self.frequency == self.DAILY:
            return start_date + timedelta(days=1)

        elif self.frequency == self.WEEKLY:
            current_day = start_date.weekday()
            days = []

            # Collect days that are greater than the current day
            for d in self.days_of_week:
                if d > current_day:
                    days.append(d)

            # Append all days of the week to complete the cycle
            days.extend(self.days_of_week)

            # Calculate days ahead for the next occurrence
            days_ahead = days[0] - current_day
            if days_ahead <= 0:
                days_ahead += 7

            return start_date + timedelta(days=days_ahead)

        elif self.frequency == self.MONTHLY:
            next_month = start_date.month + 1
            next_year = start_date.year

            if next_month > 12:
                next_month = 1
                next_year += 1

            # Determine the valid day for the next month
            next_day = min(start_date.day,
                           (date(next_year, next_month + 1, 1) - timedelta(days=1)).day)
            return date(next_year, next_month, next_day)

    def __str__(self):
<<<<<<< HEAD
        """str function"""
=======
        """
        Returns a string representation of the recurrence pattern.

        Returns:
        str: A string describing the recurrence pattern.
        """
>>>>>>> 21a72f62f97f3a87945109bc740b077be221c049
        if self.frequency == self.DAILY:
            return "Every day"
        elif self.frequency == self.WEEKLY:
            if self.days_of_week:
                days_string = ""
                for i, day in enumerate(self.days_of_week):
                    days_string += self.DAY_NAMES[day]
                    if i < len(self.days_of_week) - 1:
                        days_string += ", "
                return f"Weekly on {days_string}"
            else:
                return "Every week"
        elif self.frequency == self.MONTHLY:
            return "Every month"


# Example usage
if __name__ == "__main__":
    # Daily recurrence
    daily_recur = RecurFrequency(RecurFrequency.DAILY)
    print(f"Daily recurrence: {daily_recur}")
    start = date(2024, 1, 1)
    print(f"Next occurrence after {start}: {daily_recur.get_next_occurrence(start)}")

    # Weekly recurrence on Sunday and Friday
    weekly_recur = RecurFrequency(RecurFrequency.WEEKLY, days_of_week=[0, 5])  # Sunday and Friday
    print(f"\nWeekly recurrence: {weekly_recur}")
    start = date(2024, 1, 3)  # A Wednesday
    print(f"Next occurrence after {start}: {weekly_recur.get_next_occurrence(start)}")

    # Monthly recurrence
    monthly_recur = RecurFrequency(RecurFrequency.MONTHLY)
    print(f"\nMonthly recurrence: {monthly_recur}")
    start = date(2024, 1, 15)
    print(f"Next occurrence after {start}: {monthly_recur.get_next_occurrence(start)}")

    # Limited weekly recurrence with an end date
    end_date = date(2024, 1, 31)  # End of January
    limited_weekly_recur = RecurFrequency(RecurFrequency.WEEKLY, end_date=end_date, days_of_week=[0, 5])  # Sundays and Fridays
    print(f"\nLimited weekly recurrence: {limited_weekly_recur}")
    start = date(2024, 1, 1)  # Starting on a Monday
    next_occurrence = start
    while next_occurrence:
        next_occurrence = limited_weekly_recur.get_next_occurrence(next_occurrence)
        if next_occurrence:
            print(f"Next occurrence after {start}: {next_occurrence}")
            start = next_occurrence  # Update start for the next iteration
