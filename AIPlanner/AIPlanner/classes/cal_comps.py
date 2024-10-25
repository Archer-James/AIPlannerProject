import reflex as rx
from AIPlanner.classes.CreateCal import GenCalendar
from AIPlanner.classes.WeeklyCal import GenWeeklyCal

class cal_comps():

    def calendar_component():
        """
        Calendar initializer and caller
        """
        return rx.vstack(
            # Navigation buttons for previous and next months

            rx.hstack(
                rx.link(
                    rx.button("Weekly"),
                    href="/weekly",
                    is_external=False,
                ), 
                rx.heading(GenCalendar.label, size = "lg"), 
                rx.button("Previous", on_click=GenCalendar.prev_month),
                rx.button("Next", on_click=GenCalendar.next_month),
            ),
    
            # Create the table for the calendar
            

            # Table header for days of the week
            rx.table.root(

                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Sun", scope = "col"),
                        rx.table.column_header_cell("Mon",scope = "col"),
                        rx.table.column_header_cell("Tues",scope = "col"),
                        rx.table.column_header_cell("Wed",scope = "col"),
                        rx.table.column_header_cell("Thurs",scope="col"),
                        rx.table.column_header_cell("Fri",scope = "col"),
                        rx.table.column_header_cell("Sat",scope = "col"),
                        )
                    ),

                    # Table body for days in the month
                rx.table.body(
                    rx.foreach(GenCalendar.dates, lambda week: rx.table.row(
                        rx.foreach(week, lambda day: rx.table.cell(day, text_align="center", padding="10px"))
        ))),
            ),
            width="100%",

                padding="20px",
            ),

    def weekly_component():
        """
        Calendar initializer and caller
        """
        return rx.vstack(
            # Navigation buttons for previous and next months

            rx.hstack(
                rx.link(
                    rx.button("Monthly"),
                    href="/",
                    is_external=False,
                ), 
                rx.heading(GenWeeklyCal.label, size = "lg"), 
                rx.button("Previous", on_click=GenWeeklyCal.prev_week),
                rx.button("Next", on_click=GenWeeklyCal.next_week),
            ),
    
            # Create the table for the calendar
            

            # Table header for days of the week
            rx.table.root(

                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Sun", scope = "col"),
                        rx.table.column_header_cell("Mon",scope = "col"),
                        rx.table.column_header_cell("Tues",scope = "col"),
                        rx.table.column_header_cell("Wed",scope = "col"),
                        rx.table.column_header_cell("Thurs",scope="col"),
                        rx.table.column_header_cell("Fri",scope = "col"),
                        rx.table.column_header_cell("Sat",scope = "col"),
                        )

                    ),

                    # Table body for days in the month
                rx.table.body(
                    rx.foreach(GenWeeklyCal.dates, lambda week: rx.table.row(
                        rx.foreach(week, lambda day: rx.table.cell(day, text_align="center", padding="10px"))
        ))),
            ),
            width="100%",

                padding="20px",
            ),