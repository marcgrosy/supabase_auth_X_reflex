import reflex as rx
from typing import Optional
from gotrue import SyncSupportedStorage
import logging
import os
from supabase import create_client, Client, ClientOptions
import time

logger = logging.getLogger(__name__)


class ReflexCookieStorage(rx.State, SyncSupportedStorage):
    """A storage implementation that uses Reflex's Cookie state to store session data."""

    auth_storage: str = rx.Cookie("", name="auth_storage")

    def get_item(self, key: str) -> str | None:
        """Get an item from storage."""
        try:
            if not self.auth_storage:
                return None
            data = self.auth_storage
            logger.info(f"Current keys in auth_storage: {list(self.auth_storage['toplevel'].keys())}")
            return data["toplevel"].get(key)
        except Exception as e:
            logger.error(f"Error getting storage item: {e}. Key: {key}")
            return None

    def set_item(self, key: str, value: str) -> None:
        """Set an item in storage."""
        logger.info(f"Setting storage item: {key} = {value}")
        try:
            current_data = {"toplevel": {}}
            if self.auth_storage and self.auth_storage["toplevel"]:
                current_data = self.auth_storage
            current_data["toplevel"][key] = value
            self.auth_storage = current_data
            logger.info(f"Current keys in auth_storage: {list(self.auth_storage['toplevel'].keys())}")
        except Exception as e:
            logger.error(f"Error setting storage item: {e}. Key: {key}, Value: {value}")

    def remove_item(self, key: str) -> None:
        """Remove an item from storage."""
        try:
            if not self.auth_storage:
                return
            current_data = self.auth_storage
            if key in current_data["toplevel"]:
                del current_data["toplevel"][key]
                self.auth_storage = current_data
            logger.info(f"Current keys in auth_storage: {list(self.auth_storage['toplevel'].keys())}")
        except Exception as e:
            logger.error(f"Error removing storage item: {e}. Key: {key}")


supabase_url: str = f"https://{os.environ.get('SUPABASE_IDENTIFIER')}.supabase.co"
supabase_key: str = os.environ.get("SUPABASE_KEY")


class AuthState(rx.State):
    """The app state."""

    # Only store serializable data in state
    user_email: Optional[str] = None
    user_id: Optional[str] = None
    email: str = ""
    password: str = ""
    full_name: str = ""
    user_name: Optional[str] = None
    view_type: str = "login"
    input_password_type: str = "password"
    is_loading: bool = False

    async def get_supabase_client(self) -> Client:
        """Get a Supabase client with the current session storage."""
        reflex_cookie_storage = await self.get_state(ReflexCookieStorage)
        client = create_client(
            supabase_url, supabase_key, ClientOptions(storage=reflex_cookie_storage)
        )
        return client

    def toggle_show_password(self):
        self.input_password_type = (
            "password" if self.input_password_type == "text" else "text"
        )

    def set_full_name(self, full_name: str):
        self.full_name = full_name

    def handle_submit(self, form_data: dict):
        self.is_loading = True
        time.sleep(0.2)

        if self.view_type == "login":
            return self.sign_in()
        elif self.view_type == "signup":
            return self.sign_up()
        elif self.view_type == "forgot_password":
            return self.reset_password()

    async def sign_up(self):
        try:
            if os.environ.get("LOCAL"):
                redirect_to = f"http://{os.environ.get('DOMAIN')}"
            else:
                redirect_to = f"https://{os.environ.get('DOMAIN')}"

            client = await self.get_supabase_client()
            response = client.auth.sign_up(
                {
                    "email": self.email,
                    "password": self.password,
                    "options": {
                        "data": {
                            "full_name": self.full_name,
                        },
                        "email_redirect_to": redirect_to,
                    },
                }
            )
        except Exception as e:
            yield rx.toast.error(str(e), position="top-right", duration=10000)
            return

        self.reset_form()
        self.is_loading = False
        yield rx.toast.success(
            "Check your email to verify your account and log in!",
            position="top-right",
            duration=10000,
        )

    def set_login_view(self):
        self.view_type = "login"

    def set_signup_view(self):
        self.view_type = "signup"

    def set_forgot_password_view(self):
        self.view_type = "forgot_password"

    def reset_form(self):
        self.email = ""
        self.password = ""
        self.full_name = ""

    async def sign_in(self):
        try:
            client = await self.get_supabase_client()
            response = client.auth.sign_in_with_password(
                {"email": self.email, "password": self.password}
            )
        except Exception as e:
            self.is_loading = False
            yield rx.toast.error(str(e), position="top-right", duration=10000)
            return

        self.is_loading = False
        if response.user:
            self.user_email = response.user.email
            self.user_id = response.user.id
            self.user_name = (
                response.user.user_metadata.get("full_name")
                or response.user.user_metadata.get("name")
                or response.user.email.split("@")[0]
            )

            self.email = ""
            self.password = ""
        else:
            yield rx.toast.error(
                "Invalid email or password", position="top-right", duration=10000
            )

    def start_loading(self):
        self.is_loading = True
        yield

    async def sign_in_with_oauth(self, provider: str):
        try:
            redirect_to = (
                "http://localhost:3000"
                if os.getenv("LOCAL") == "true"
                else f"https://{os.environ.get('DOMAIN')}"
            )

            options = {
                "redirect_to": redirect_to,
            }

            client = await self.get_supabase_client()
            response = client.auth.sign_in_with_oauth(
                {
                    "provider": provider,
                    "options": options,
                }
            )
        except Exception as e:
            self.is_loading = False
            yield rx.toast.error(str(e), position="top-right", duration=10000)
            return

        self.is_loading = False
        yield rx.redirect(response.url)

    async def reset_password(self):
        try:
            client = await self.get_supabase_client()
            response = client.auth.reset_password_for_email(
                self.email,
                {
                    "redirect_to": "http://localhost:3000/update-password",
                },
            )

            self.is_loading = False
            yield rx.toast.success(
                "Password reset email sent. Please check your inbox.",
                position="top-right",
                duration=10000,
            )
        except Exception as e:
            self.is_loading = False
            yield rx.toast.error(str(e), position="top-right", duration=10000)

    async def check_auth(self):
        params = self.router.page.params
        logger.info(f"Params: {params}")
        # Parse URL fragment if params are empty
        if not params and "#" in self.router.page.raw_path:
            fragment = self.router.page.raw_path.split("#", 1)[1]
            params = dict(param.split("=") for param in fragment.split("&"))

        if "error_description" in params:
            readable_error = params["error_description"].replace("+", " ")
            yield rx.toast.error(readable_error, position="top-right", duration=10000)

        session = None
        client = await self.get_supabase_client()

        # Handle signup confirmation
        if "access_token" in params and "refresh_token" in params:
            try:
                client.auth.set_session(params["access_token"], params["refresh_token"])

                # Remove the tokens from the URL
                yield rx.redirect("/")
            except Exception as e:
                logger.error(f"Error setting session from URL params: {e}")
                yield rx.toast.error(
                    "Error confirming signup. Please try again.",
                    position="top-right",
                    duration=10000,
                )

        # Handle OAuth callback
        if "code" in params:
            logger.info(f"Code received: {params['code']}")
            try:
                # Log the request details
                logger.info(
                    f"Attempting to exchange code for session with params: {params}"
                )

                # Create a new session with the auth code
                auth_response = client.auth.exchange_code_for_session(
                    {"auth_code": params["code"]}
                )

                client.auth.set_session(
                    auth_response.session.access_token,
                    auth_response.session.refresh_token,
                )

                # Log successful session creation
                logger.info(f"Session created successfully: {auth_response.session}")

                yield rx.redirect("/")
            except Exception as e:
                # Log detailed error information
                logger.error(
                    f"Error exchanging code for session: {e}",
                    exc_info=True,
                    extra={
                        "params": params,
                        "error_type": type(e).__name__,
                    },
                )

        session = client.auth.get_session()

        if session and session.access_token:
            try:
                response = client.auth.get_user(session.access_token)
                if response and response.user:
                    token_user_id = client.auth.get_user(session.access_token).user.id
                    if token_user_id != response.user.id:
                        raise Exception("User ID mismatch")

                    self.user_email = response.user.email
                    self.user_id = response.user.id
                    self.user_name = (
                        response.user.user_metadata.get("full_name")
                        or response.user.user_metadata.get("name")
                        or response.user.email.split("@")[0]
                    )
                else:
                    # pass
                    self.clear_user_data()
            except Exception as e:
                logger.error(f"Error getting user: {e}")
                # pass
                self.clear_user_data()
        else:
            # pass
            self.clear_user_data()
            yield rx.redirect("/")

    def clear_user_data(self):
        self.user_email = None
        self.user_id = None
        self.user_name = None

    async def sign_out(self):
        try:
            client = await self.get_supabase_client()
            client.auth.sign_out()
        except Exception as e:
            logger.error(f"Error signing out: {e}")
        finally:
            self.clear_user_data()
            yield rx.redirect("/")
