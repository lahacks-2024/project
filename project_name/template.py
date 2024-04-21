from typing import Callable

import reflex as rx

from project_name.navigation import dashboard_sidebar
from project_name.styles import BACKGROUND_COLOR, FONT_FAMILY


def template(page: Callable[[], rx.Component]) -> rx.Component:
    return rx.box(
        dashboard_sidebar,
        page(),
        rx.box (
            rx.logo(),
            class_name="absolute bottom-0 w-full",
        ),
        background_color=BACKGROUND_COLOR,
        font_family=FONT_FAMILY,
        padding_bottom="4em",
        class_name="flex h-screen"
    )
