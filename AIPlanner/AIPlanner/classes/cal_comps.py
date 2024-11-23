import reflex as rx
from AIPlanner.classes.CreateCal import GenCalendar
from AIPlanner.classes.WeeklyCal import GenWeeklyCal
from AIPlanner.classes.daily_cal import daily_cal


def calendar_component():
    """
    Monthly calendar initializer and caller

    Returns:
    prints monthly calendar component
    """
    return rx.vstack(
        # Navigation buttons for previous and next months
        rx.hstack(
            rx.link(
                rx.button("Weekly"),
                href="/weekly",
                is_external=False,
            ),
            rx.heading(GenCalendar.label, size="lg"),
            rx.button("Previous", on_click=GenCalendar.prev_month),
            rx.button("Next", on_click=GenCalendar.next_month),
        ),
        # Create the table for the calendar
        # Table header for days of the week
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Sun", scope="col"),
                    rx.table.column_header_cell("Mon", scope="col"),
                    rx.table.column_header_cell("Tues", scope="col"),
                    rx.table.column_header_cell("Wed", scope="col"),
                    rx.table.column_header_cell("Thurs", scope="col"),
                    rx.table.column_header_cell("Fri", scope="col"),
                    rx.table.column_header_cell("Sat", scope="col"),
                )
            ),
            # Table body for days in the month
            rx.table.body(
                rx.foreach(GenCalendar.dates, lambda week: rx.table.row(
                    rx.foreach(week, lambda day: 
                        # Skip rendering 0
                        rx.cond(
                            day != 0,  # Check if the day is not 0
                            rx.table.cell(
                                rx.link(
                                    day,
                                    href="/daily",
                                    on_click=lambda: daily_cal.set_date(
                                        GenCalendar.current_month,
                                        GenCalendar.current_year, day),
                                    text_align="center",
                                    padding="10px"
                                )
                            ),
                            rx.table.cell()  # Render an empty cell for 0
                        )
                    )
                )),
            ),
            width="100%",
            padding="20px",
        ),
    )

def weekly_component():
    """
    Weekly calendar initializer and caller

    Returns:
    prints weekly calendar component
    """
    return rx.vstack(
        # Navigation buttons for previous and next months
        rx.hstack(
            rx.link(
                rx.button("Monthly"),
                href="/",
                is_external=False,
            ), 
            rx.heading(GenWeeklyCal.label, size="lg"), 
            rx.button("Previous", on_click=GenWeeklyCal.prev_week),
            rx.button("Next", on_click=GenWeeklyCal.next_week),
        ),
        # Create the table for the calendar
        # Table header for days of the week
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Sun", scope="col"),
                    rx.table.column_header_cell("Mon", scope="col"),
                    rx.table.column_header_cell("Tues", scope="col"),
                    rx.table.column_header_cell("Wed", scope="col"),
                    rx.table.column_header_cell("Thurs", scope="col"),
                    rx.table.column_header_cell("Fri", scope="col"),
                    rx.table.column_header_cell("Sat", scope="col"),
                )
            ),
            # Table body for days in the month
            rx.table.body(
                rx.foreach(GenWeeklyCal.dates, lambda week: rx.table.row(
                    rx.foreach(week, lambda day:
                        # Skip rendering 0
                        rx.cond(
                            day != 0,  # Check if the day is not 0
                            rx.table.cell(
                                rx.link(
                                    day,
                                    href="/daily",
                                    on_click=lambda: daily_cal.set_date(GenWeeklyCal.current_year, GenWeeklyCal.current_month, day),
                                    text_align="center",
                                    padding="10px"
                                )
                            ),
                            rx.table.cell()  # Render an empty cell for 0
                        )
                    )
                )),
            ),
            width="100%",
            padding="20px",
        ),
    )
