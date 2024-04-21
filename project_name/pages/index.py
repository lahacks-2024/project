"""The main index page."""

import reflex as rx
from project_name.navigation import navbar
from project_name.template import template
from project_name.pages.forms import forms
from project_name.data import stat_card_data, summary_data, notes_data
from typing import List

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

def summary_card(title: str, stat) -> rx.Component:
    return card(
        rx.hstack(
            rx.vstack(
                rx.text(title),
                rx.chakra.stat(
                    rx.hstack(
                        rx.chakra.stat_label(stat, color="black"),
                    ),
                ),
            ),
        ),
    )

def notes_card(title: str, notes: List[str]) -> rx.Component:
    notes_components = [
        rx.chakra.stat(
            rx.hstack(
                rx.chakra.stat_label("- " + note, color="black"),
            ),
        )
        for note in notes
    ]
    return card(
        rx.hstack(
            rx.vstack(
                rx.text(title),
                *notes_components,
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
        row_gap=4,
    )

def content_grid2():
    return rx.chakra.grid(
        *[
            rx.chakra.grid_item(summary_card(*c), col_span=1, row_span=1)
            for c in summary_data
        ],
        *[
            rx.chakra.grid_item(notes_card(*c), col_span=1, row_span=1)
            for c in notes_data
        ],
        template_columns="repeat(2, 1fr)",
        width="100%",
        gap=4,
        row_gap=4,
    )


@template
def index() -> rx.Component:
    return rx.box(
            navbar(heading="Dashboard"),
            rx.box(
                content_grid(),
                class_name="pt-24 pb-4 px-8",
            ),
            rx.box(
                content_grid2(),
                class_name="pb-8 px-8",
            ),
            padding_left="250px",
            class_name="max-[800px]:!pl-0",
        )
