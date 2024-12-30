# Supabase Auth + Reflex Demo

This project demonstrates how to implement Supabase authentication in a [Reflex](https://reflex.dev) web application. It includes both email/password and Google OAuth authentication methods.

## Prerequisites

- Python 3.8 or higher
- Basic understanding of Python
- A Supabase account (free tier works fine)

## Setup Instructions

### 1. Create a Supabase Project

1. Go to [Supabase](https://supabase.com) and sign up/login
2. Create a new project
3. Once created, go to Project Settings -> API to find your project credentials

### 2. Configure Environment Variables

1. Copy the example environment file:
```
cp .env.example .env
```


2. In your `.env` file, fill in the following values from your Supabase project:
- `SUPABASE_IDENTIFIER`: Your project identifier (e.g., from "https://x123456789x.supabase.co" take "x123456789x")
- `SUPABASE_PASSWORD`: Your project's database password
- `SUPABASE_KEY`: Your project's anon/public key

### 3. Set Up Python Environment

1. Create and activate a virtual environment:
```
python3 -m venv .venv
source .venv/bin/activate # On Windows, use: .venv\Scripts\activate
```

2. Install dependencies:
```
# Option 1: Using pip
pip install -r requirements.txt

# Option 2: Using uv (faster)
uv pip install -r requirements.txt

# Optional: Recompile requirements
uv pip compile requirements.in -o requirements.txt
```


### 4. Run the Application

1. Start the Reflex development server:
```
reflex run
```

2. Open your browser and navigate to [http://localhost:3000](http://localhost:3000)


## Testing Authentication

1. **Email/Password Authentication**:
   - Click "Sign Up" to create a new account
   - Use your email and a password
   - Verify confirmation email
   - You should be able to log in successfully
   - You should be automatically logged in and see the protected main page
   - should also be logged in automatically on other tabs but not when re-opening the browser for whatever reason

2. **Google Authentication**:
   - Click the Google sign-in button
   - Note: Currently experiencing some cookie-related issues with Google auth and email/password auth

## Known Issues

- Has some cookie-handling issues that are being investigated
- Email/password authentication is working better than Google auth

## Learn More

- [Reflex Documentation](https://reflex.dev/docs/getting-started/introduction/)
- [Supabase Python Docs](https://supabase.com/docs/reference/python/start)

The Discord of both Supabase and Reflex are very active and the mods are very helpful.

## Repository Structure and Code Overview

The main application code is located in the `supabase_auth_X_reflex/` directory. Here's how the code is organized:

### Key Files

- `supabase_auth_X_reflex.py`: The main entry point of the application. It determines which component to show based on the authentication state.
- `auth_state.py`: Manages the authentication state using Reflex's State class.
- `auth_component.py`: The login/signup UI component shown to unauthenticated users.
- `main_app_component.py`: The protected content shown to authenticated users (currently contains dummy content).

### Application Flow

The app follows a simple authentication flow:

1. When a user visits the site, the app checks for a user_id in the AuthState
2. If no user_id is found (user not authenticated):
   - The `auth_component` is displayed
   - User can choose to login with email/password or Google
3. If user_id exists (user is authenticated):
   - The `mainApp` component is displayed
   - Currently shows placeholder content for demonstration
