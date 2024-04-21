"""The main index page."""

import reflex as rx
from project_name.navigation import navbar
from project_name.template import template
# from project_name.pages.forms import forms
from project_name.data import stat_card_data

def card(*children, **props):
    return rx.card(
        *children,
        box_shadow="rgba(0, 0, 0, 0.1) 0px 4px 6px -1px, rgba(0, 0, 0, 0.06) 0px 2px 4px -1px;",
        **props,
    )

# Content in a grid layout.
def stat_card(title: str, stat, delta) -> rx.Component:
    color = "var(--red-9)" if delta[0] == "-" else "var(--green-9)"
    arrow = "decrease" if delta[0] == "-" else "increase"
    return card(
        rx.hstack(
            rx.vstack(
                rx.text(title),
                rx.chakra.stat(
                    rx.hstack(
                        rx.chakra.stat_number(stat, color=color),
                        rx.chakra.stat_help_text(
                            rx.chakra.stat_arrow(type_=arrow), delta[1:]
                        ),
                    ),
                ),
            ),
        ),
    )


def content_grid():
    return rx.chakra.grid(
        *[
            rx.chakra.grid_item(stat_card(*c), col_span=1, row_span=1)
            for c in stat_card_data
        ],
        template_columns="repeat(4, 1fr)",
        width="100%",
        gap=4,
        row_gap=8
    )


@template
def index() -> rx.Component:
    return rx.box(
            navbar(heading="Dashboard"),
            rx.box(
                content_grid(),
                class_name="pt-24 pb-8 px-8",
            ),
            padding_left="250px",
            
        )
