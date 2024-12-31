from nicegui import ui, app
from pathlib import Path
from dotenv import load_dotenv
from login import setup_login_page, check_session
import os
import cards

# Load environment variables
load_dotenv()

@ui.page('/')
def home():
    setup_login_page()

# Run the app
port = int(os.getenv('PORT', 8082))
ui.run(
    port=port,
    storage_secret=os.getenv(
        'STORAGE_SECRET', 'generate_a_secure_random_key_and_store_in_env'),
    host='0.0.0.0')
