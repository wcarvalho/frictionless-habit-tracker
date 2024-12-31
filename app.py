from nicegui import ui, app
from pathlib import Path
from dotenv import load_dotenv
import os
import authentication
import cards
from datetime import datetime, timedelta
from firebase import db
import asyncio
import habits
# Load environment variables
load_dotenv()

@ui.page('/')
def home():
    card = cards.default()
    # Add flex layout to the card itself
    card.classes('flex flex-col h-full')
    with card:
        # Top section with welcome message
        if not app.storage.user.get('logged_in', False):
            ui.button('Login with Google',
                    on_click=lambda: ui.navigate.to(authentication.start_oauth()))
        else:
            # Welcome message section with logout button
            with ui.element('div').classes('mb-4 flex justify-between items-center'):
                with ui.row().classes('w-full'):
                  ui.label(f'Welcome back, {app.storage.user.get("email")}!')
                  ui.space()
                  ui.button('Logout', on_click=authentication.logout)
            
            # Middle section with tabs (will expand to fill available space)
            with ui.element('div').classes('flex-grow flex flex-col w-full min-h-0'):
                with ui.tabs().classes('w-full') as tabs:
                    habits_tab = ui.tab('Habits')
                    history_grid_tab = ui.tab('History Grid')
                    graph_tab = ui.tab('Graph')
                # Add flex-grow and min-h-0 to tab panels to allow proper expansion
                with ui.tab_panels(tabs, value=habits_tab).classes('w-full flex-grow min-h-0'):
                    with ui.tab_panel(habits_tab).classes('h-full'):
                        habits.page()
                    with ui.tab_panel(history_grid_tab).classes('h-full'):
                        ui.label('History Grid')
                    with ui.tab_panel(graph_tab).classes('h-full'):
                        ui.label('Graph')

@ui.page('/test-firebase')
def test_firebase():
    try:
        # Try to write a test document
        doc_ref = db.collection('test').document('test')
        doc_ref.set({'test': 'successful'})
        ui.label('Firebase connection successful!')
    except Exception as e:
        ui.label(f'Firebase error: {str(e)}')

# Run the app
port = int(os.getenv('PORT', 8082))
ui.run(
    port=port,
    storage_secret=os.getenv('STORAGE_SECRET', 'generate_a_secure_random_key_and_store_in_env'),
    host='0.0.0.0')
