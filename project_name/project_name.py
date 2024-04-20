"""The main Dashboard App."""

from rxconfig import config

import reflex as rx

from project_name.styles import BACKGROUND_COLOR, FONT_FAMILY, THEME, STYLESHEETS

from project_name.pages.tools import tools
from project_name.pages.team import team
from project_name.pages.index import index
from project_name.pages.forms import forms

# Create app instance and add index page.
app = rx.App(
    theme=THEME,
    stylesheets=STYLESHEETS,
)

app.add_page(index, route="/")
app.add_page(tools, route="/tools")
app.add_page(team, route="/team")
app.add_page(forms)
