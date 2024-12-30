import reflex as rx
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

config = rx.Config(
    app_name="supabase_auth_X_reflex",
)