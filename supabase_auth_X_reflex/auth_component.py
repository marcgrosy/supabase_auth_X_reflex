import reflex as rx
from supabase_auth_X_reflex.auth_state import AuthState


def email_input() -> rx.Component:
    return (
        rx.box(
            rx.text("Email address", size="2", margin_bottom="2px", weight="bold"),
            rx.hstack(
                rx.input(
                    on_change=AuthState.set_email,
                    box_shadow="none",
                    style={"outline": "none"},
                    width="100%",
                ),
                border=f"1px solid {rx.color('gray', 5)}",
                border_radius="10px",
                align_items="center",
                justify="center",
                _focus_within={"box_shadow": f"0 0 5px {rx.color('gray', 7)}"},
            ),
            width="100%",
        ),
    )


def password_input() -> rx.Component:
    return (
        rx.box(
            rx.text("Password", size="2", margin_bottom="2px", weight="bold"),
            rx.hstack(
                rx.input(
                    type=rx.cond(
                        AuthState.input_password_type == "text", "text", "password"
                    ),
                    on_change=AuthState.set_password,
                    box_shadow="none",
                    style={"outline": "none"},
                    width="100%",
                ),
                rx.spacer(),
                rx.icon(
                    tag="eye",
                    class_name="cursor-pointer",
                    size=25,
                    color=rx.color("gray", 9),
                    padding_right="10px",
                    on_click=AuthState.toggle_show_password,
                ),
                border=f"1px solid {rx.color('gray', 5)}",
                border_radius="10px",
                align_items="center",
                justify="center",
                _focus_within={"box_shadow": f"0 0 5px {rx.color('gray', 7)}"},
            ),
            rx.cond(
                AuthState.view_type == "login",
                rx.box(
                    rx.link(
                        "Forgot Password?",
                        on_click=AuthState.set_forgot_password_view,
                        color=rx.color("accent", 9),
                        size="2",
                        margin_bottom="3",
                        width="100%",
                    ),
                    text_align="right",
                ),
            ),
            width="100%",
        ),
    )


def continue_button() -> rx.Component:
    return (
        rx.hstack(
            rx.button(
                "Continue",
                rx.icon(tag="play", size=10, stroke_width=3),
                type="submit",
                on_click=AuthState.start_loading(),
                width="100%",
                loading=AuthState.is_loading,
            ),
            width="100%",
            margin_bottom="3",
        ),
    )


def google_button() -> rx.Component:
    return (
        rx.button(
            rx.image(src="/google.svg"),
            "Continue with Google",
            color=rx.color("gray", 11),
            background_color=rx.color("gray", 1),
            border=f"1px solid {rx.color('gray', 5)}",
            on_click=[
                AuthState.start_loading(),
                AuthState.sign_in_with_oauth("google"),
            ],
            _hover={
                "background_color": rx.color("gray", 3),
                "transition": "all 0.2s ease-in-out",
            },
            box_shadow=f"0 0 5px {rx.color('gray', 5)}",
        ),
    )


def or_separator() -> rx.Component:
    return (
        rx.hstack(
            rx.separator(),
            rx.text("or", color=rx.color("gray", 8), size="2"),
            rx.separator(),
            justify="center",
            align="center",
            padding="5px 0px",
        ),
    )


def login_component() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.vstack(
                rx.box(
                    rx.heading(
                        "Sign in via Supabase",
                        size="3",
                        margin_bottom="6px",
                    ),
                    rx.text(
                        "Welcome back! Please sign in to continue",
                        color=rx.color("gray", 11),
                        size="2",
                    ),
                    text_align="center",
                ),
                google_button(),
                or_separator(),
                rx.form(
                    rx.vstack(
                        email_input(),
                        password_input(),
                        continue_button(),
                        spacing="6",
                    ),
                    on_submit=AuthState.handle_submit,
                ),
                rx.separator(),
                rx.text(
                    "Don't have an account? ",
                    rx.link(
                        "Sign Up",
                        on_click=AuthState.set_signup_view,
                        color=rx.color(
                            "accent",
                            9,
                        ),
                    ),
                    size="2",
                    color=rx.color("gray", 11),
                    text_align="center",
                ),
                width="390px",
                spacing="6",
                align_items="stretch",
                border=f"1px solid {rx.color('gray', 6)}",
                box_shadow=f"0 0 20px {rx.color('gray', 6)}",
                border_radius="10px",
                padding="40px",
            ),
            margin_top="10vh",
        ),
        align_items="flex-start",
        height="100vh",
    )


def signup_component() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.vstack(
                rx.box(
                    rx.heading(
                        "Create your Supabase account",
                        size="3",
                        margin_bottom="6px",
                    ),
                    rx.text(
                        "Welcome! Please fill in the details to get started.",
                        color=rx.color("gray", 11),
                        size="2",
                    ),
                    text_align="center",
                ),
                google_button(),
                or_separator(),
                rx.box(
                    rx.text("First name", size="2", margin_bottom="2px", weight="bold"),
                    rx.hstack(
                        rx.input(
                            on_change=AuthState.set_full_name,
                            box_shadow="none",
                            style={"outline": "none"},
                            width="100%",
                        ),
                        border=f"1px solid {rx.color('gray', 5)}",
                        border_radius="10px",
                        align_items="center",
                        justify="center",
                        _focus_within={"box_shadow": f"0 0 5px {rx.color('gray', 7)}"},
                    ),
                ),
                rx.form(
                    rx.vstack(
                        email_input(),
                        password_input(),
                        continue_button(),
                        spacing="6",
                    ),
                    on_submit=AuthState.handle_submit,
                ),
                rx.separator(),
                rx.text(
                    "Already have an account? ",
                    rx.link(
                        "Sign In",
                        on_click=AuthState.set_login_view,
                        color=rx.color(
                            "accent",
                            9,
                        ),
                    ),
                    size="2",
                    color=rx.color("gray", 11),
                    text_align="center",
                ),
                width="390px",
                spacing="6",
                align_items="stretch",
                border=f"1px solid {rx.color('gray', 6)}",
                box_shadow=f"0 0 20px {rx.color('gray', 6)}",
                border_radius="10px",
                padding="40px",
            ),
            margin_top="10vh",
        ),
        align_items="flex-start",
        height="100vh",
    )


def forgot_password_component() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.vstack(
                rx.box(
                    rx.heading(
                        "Reset your password",
                        size="3",
                        margin_bottom="6px",
                    ),
                    rx.text(
                        "We'll send you a link to reset your password.",
                        color=rx.color("gray", 11),
                        size="2",
                    ),
                    text_align="center",
                ),
                rx.form(
                    rx.vstack(
                        email_input(),
                        continue_button(),
                        spacing="6",
                    ),
                    on_submit=AuthState.handle_submit,
                ),
                or_separator(),
                google_button(),
                rx.separator(),
                rx.text(
                    "",
                    rx.link(
                        "Back",
                        on_click=AuthState.set_login_view,
                        color=rx.color(
                            "accent",
                            9,
                        ),
                    ),
                    size="2",
                    color=rx.color("gray", 11),
                    text_align="center",
                ),
                width="390px",
                spacing="6",
                align_items="stretch",
                border=f"1px solid {rx.color('gray', 6)}",
                box_shadow=f"0 0 20px {rx.color('gray', 6)}",
                border_radius="10px",
                padding="40px",
            ),
            margin_top="10vh",
        ),
        align_items="flex-start",
        height="100vh",
    )


def auth_component() -> rx.Component:
    return rx.cond(
        AuthState.view_type == "login",
        login_component(),
        rx.cond(
            AuthState.view_type == "signup",
            signup_component(),
            forgot_password_component(),
        ),
    )
