import reflex as rx
from reflex.components import lucide

from project_name.styles import FONT_FAMILY


def sidebar_link(text: str, href: str, icon: str):
    return rx.link(
        rx.flex(
            rx.icon_button(
                rx.icon(tag=icon, weight=16, height=16),
                variant="soft",
            ),
            text,
            py="2",
            px="4",
            spacing="3",
            align="baseline",
            direction="row",
            font_family=FONT_FAMILY,
        ),
        href=href,
        width="100%",
        border_radius="8px",
        _hover={
            "background": "rgba(255, 255, 255, 0.1)",
            "backdrop_filter": "blur(10px)",
        },
    )


def sidebar(
    *sidebar_links,
    **props,
) -> rx.Component:
    logo_src = props.get("logo_src", "/logo.jpg")
    heading = props.get("heading", "NOT SET")
    return rx.vstack(
        rx.hstack(
            rx.image(
                src=logo_src, 
                height="100%", 
                border_radius="8px",
                class_name="flex justify-center items-center content-center"
            ),
            rx.heading(
                heading,
                font_family=FONT_FAMILY,
                size="7",
                height="100%",
                class_name="flex justify-center items-center content-center"
            ),
            width="100%",
            spacing="7",
            class_name="flex flex-row justify-center items-center content-center h-10",
        ),
        rx.divider(margin_y="3"),
        rx.vstack(
            *sidebar_links,
            padding_y="1em",
        ),
        width="250px",
        position="fixed",
        height="100%",
        left="0px",
        top="0px",
        align_items="left",
        z_index="10",
        backdrop_filter="blur(10px)",
        padding="2em",
        class_name="max-[800px]:!hidden",
    )


dashboard_sidebar = sidebar(
    sidebar_link(text="Dashboard", href="/", icon="bar_chart_3"),
    sidebar_link(text="Favorites", href="/favorites", icon="star"),
    logo_src="/icon.png",
    heading="VERSA",
    class_name="flex flex-row justify-center items-center content-center",
)


class State(rx.State):
    pass


def navbar(heading: str) -> rx.Component:
    return rx.hstack(
        rx.heading(heading, font_family=FONT_FAMILY, size="7"),
        rx.spacer(),
        rx.menu.root(
            rx.menu.trigger(
                rx.button(
                    "Menu",
                    lucide.icon(tag="chevron_down", weight=16, height=16),
                    font_family=FONT_FAMILY,
                    variant="soft",
                ),
            ),
            rx.menu.content(
                rx.menu.item("Settings"),
                rx.menu.item("Profile"),
                rx.menu.item("Logout"),
                font_family=FONT_FAMILY,
                variant="soft",
            ),
            variant="soft",
            font_family=FONT_FAMILY,
        ),
        position="fixed",
        width="calc(100% - 250px)",
        top="0px",
        z_index="1000",
        padding_x="2em",
        padding_top="2em",
        padding_bottom="1em",
        backdrop_filter="blur(10px)",
        class_name="max-[800px]:!w-screen"
    )
