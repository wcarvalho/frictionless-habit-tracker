from nicegui import ui, app
from pathlib import Path
from dotenv import load_dotenv
import os
import authentication
import cards

# Load environment variables
load_dotenv()

@ui.page('/')
def home():

    card = cards.default()
    with card:
      if not app.storage.user.get('logged_in', False):
        ui.button('Login with Google',
                  on_click=lambda: ui.navigate.to(authentication.start_oauth()))
      else:
        ui.label(f'Welcome back, {app.storage.user.get("email")}!')
        ui.button('Logout', on_click=authentication.logout)

# Run the app
port = int(os.getenv('PORT', 8082))
ui.run(
    port=port,
    storage_secret=os.getenv(
        'STORAGE_SECRET', 'generate_a_secure_random_key_and_store_in_env'),
    host='0.0.0.0')
