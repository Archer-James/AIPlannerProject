import reflex as rx
from AIPlanner.CreateCal import GenCalendar
from AIPlanner.WeeklyCal import GenWeeklyCal


class Cals(rx.State):
    
    @classmethod
    def cals_init(cls):
        GenCalendar.init_calendar()
        GenWeeklyCal.init_week()

        