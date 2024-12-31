from nicegui import ui, app
import firebase
from datetime import datetime, timedelta

HISTORY_LENGTH = 14


def page():
    # Create light theme styling
    ui.add_head_html('''
        <style>
        .habit-grid {
            background-color: #ffffff;
            color: #333333;
            padding: 0.5rem;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow-x: auto;
            overflow-y: auto;
            max-height: 80vh;
            position: relative;
        }
        .habit-row {
            padding: 0.25rem;
            border-bottom: 1px solid #e0e0e0;
            display: flex;
            align-items: center;
            white-space: nowrap;
            width: max-content;
            min-width: min-content;
            -webkit-overflow-scrolling: touch;
            position: relative;
        }
        .habit-cell {
            width: 50px;
            text-align: center;
            font-size: 0.9em;
            flex: 0 0 50px;
        }
        .habit-name {
            width: 150px;
            flex-shrink: 0 0 150px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            padding-right: 10px;
            position: sticky;
            left: 0;
            background: #ffffff;
            z-index: 1;
            border-right: 1px solid #e0e0e0;
        }
        /* Added: Style for header row */
        .header-row {
            position: sticky;
            top: 0;
            background: #ffffff;
            z-index: 3;
            border-bottom: 2px solid #e0e0e0;
        }
        /* Added: Style for header cell that's both sticky left and top */
        .header-corner {
            position: sticky;
            left: 0;
            z-index: 4;
            background: #ffffff;
        }
        .color-box {
            width: 20px;
            height: 20px;
            border-radius: 4px;
            margin: auto;
        }
        </style>
    ''')

    # Create container with dark background and scrollable content
    with ui.card().classes('habit-grid').style('max-height: 500px; overflow-y: auto; margin: auto; max-width: 800px;'):
        # Update header row with proper cell structure
        with ui.row().classes('habit-row header-row'):
            ui.label('').classes('habit-cell')  # Color column header
            # Added text instead of empty label
            ui.label('Habits').classes('habit-name header-corner')
            today = datetime.now()
            for i in range(-HISTORY_LENGTH + 1, 1):
                date = today + timedelta(days=i)
                ui.label(date.strftime('%a\n%d')).classes('habit-cell')

        # Add more habits to the list
        habits = [
            ('Cardio', '#FF5722'),          # Orange
            ('Strength', '#FF5722'),
            ('Stretch', '#FF5722'),
            ('Workout', '#FF5722'),
            ('no sugar', '#4CAF50'),         # Green
            ('Read morning\n>= 20 minutes', '#4CAF50'),
            ('Read paper\n>= 20 min', '#2196F3'),  # Blue
            ('Night routine', '#2196F3'),
            ('No Junk', '#2196F3'),
            ('flash cards', '#2196F3'),
        ]

        # Define available colors
        COLOR_OPTIONS = {
            'Orange': '#FF5722',
            'Green': '#4CAF50',
            'Blue': '#2196F3',
            'Red': '#F44336',
            'Purple': '#9C27B0'
        }

        for habit_name, color in habits:
            with ui.row().classes('habit-row'):
                # Create a colored box instead of text label
                with ui.button().classes('habit-cell').style(f'background-color: {color}; min-width: 30px; min-height: 30px; padding: 0; border: 1px solid #e0e0e0') as color_box:
                    pass  # Empty button with just color
                habit_label = ui.label(habit_name).classes(
                    'habit-name').style(f'color: {color}')

                def create_color_picker(current_box, current_label):
                    async def handle_color_pick():
                        with ui.dialog() as dialog, ui.card():
                            ui.grid().classes('gap-1').style('display: grid; grid-template-columns: repeat(3, 1fr);')
                            for color_value in COLOR_OPTIONS.values():
                                def create_color_setter(new_color):
                                    def set_color():
                                        current_box.style(
                                            f'background-color: {new_color}')
                                        current_label.style(
                                            f'color: {new_color}')
                                        dialog.close()
                                    return set_color

                                ui.button().style(f'''
                                    background-color: {color_value}; 
                                    min-width: 40px; 
                                    min-height: 40px; 
                                    padding: 0;
                                    margin: 2px
                                ''').on('click', create_color_setter(color_value))
                        dialog.open()
                    return handle_color_pick

                # Store the button reference directly instead of querying
                color_box.on('click', create_color_picker(
                    color_box, habit_label))

                for _ in range(HISTORY_LENGTH):  # Changed from range(5)
                    label = ui.label('0').classes('habit-cell x-mark')
                    label.style('color: #FF0000')  # Red for zero

                    def create_click_handler(current_label):
                        async def handle_click():
                            # Create a dialog with number input
                            with ui.dialog() as dialog, ui.card():
                                input_field = ui.number(
                                    label='Enter value', value=int(current_label.text))

                                def update_value():
                                    new_value = str(int(input_field.value))
                                    current_label.text = new_value
                                    # Update styling based on value
                                    if new_value == '0':
                                        current_label.style(
                                            'color: #FF0000')  # Red for zero
                                    else:
                                        # Green for non-zero
                                        current_label.style('color: #4CAF50')
                                    dialog.close()

                                ui.button('Save', on_click=update_value)
                            dialog.open()
                        return handle_click

                    label.on('click', create_click_handler(label))
