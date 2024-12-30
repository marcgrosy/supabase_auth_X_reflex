"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from supabase_auth_X_reflex.auth_state import AuthState
from supabase_auth_X_reflex.auth_component import auth_component
from supabase_auth_X_reflex.main_app_component import mainApp


@rx.page(title="Reflex X Supabase Auth - Demo Repo")
def index() -> rx.Component:
    return rx.theme(
        rx.toast.provider(),
        rx.cond(
            AuthState.is_hydrated,
            rx.cond(
                AuthState.user_id,
                mainApp(),
                auth_component(),
            ),
            rx.center(
                rx.spinner(size="3"),
                rx.text("Loading..."),
            ),
        ),
        accent_color="green",
    )


app = rx.App()
app.add_page(index, on_load=[AuthState.check_auth])
