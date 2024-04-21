"""The style classes and constants for the Dashboard App."""

from reflex.components.radix import themes as rx

COMPANY_LOGO_URL = "https://cdn-icons-png.flaticon.com/512/9908/9908191.png"

THEME = rx.theme(
    appearance="dark",
    has_background=True,
    radius="large",
    accent_color="iris",
    scaling="100%",
    panel_background="solid",
)

STYLESHEETS = [
    "/styles.css"  # This path is relative to assets/
]

FONT_FAMILY = "Inter"
BACKGROUND_COLOR = "var(--accent-2)"
