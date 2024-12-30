import reflex as rx
from supabase_auth_X_reflex.auth_state import AuthState

def mainApp() -> rx.Component:
    """The main app that's protected by supabase auth."""
    return rx.center(
        rx.vstack(
            rx.text("Congrats! You are logged in !"),
            rx.text(f"Your Email: {AuthState.user_email}"),
            rx.button("Logout", on_click=AuthState.sign_out),
        )
    )