import reflex as rx

class daily_cal (rx.State):
    selected_date: str = ""

    def set_date(self,date):
        self.selected_date = date

def daily() -> rx.Component:
    return rx.container(
        rx.text(daily_cal.selected_date)
    )
