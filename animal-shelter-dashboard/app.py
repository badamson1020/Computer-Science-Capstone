"""Entry point for the Search and Rescue Animal Dashboard.

Responsibilities are intentionally minimal. This module creates the Dash
instance, assembles the application by importing layout and callbacks,
and starts the server. All application logic lives in the imported modules.

File structure:
    app.py          - entry point (this file)
    config.py       - shared constants, database connection, logo configuration
    layout.py       - dashboard layout and component definitions (View layer)
    callbacks.py    - callback functions and interactivity (Controller layer)
    models/
        shelter_crud.py  - MongoDB data access (Model layer)
        algorithm.py     - weighted matching algorithm (Model layer)
"""

from dash import Dash

from callbacks import register_callbacks
from layout import create_layout

# suppress_callback_exceptions=True is required because the extended search panel
# is hidden on load. Dash validates callback component IDs at startup and would
# raise exceptions for components inside the hidden panel even though they exist
# in the layout. Suppressing these exceptions allows hidden components to be
# referenced in callbacks without triggering false positive validation errors.
app = Dash(__name__, suppress_callback_exceptions=True)

# Assign the layout and register callbacks after the app instance is created.
# Both layout.py and callbacks.py receive the app instance to avoid circular imports.
app.layout = create_layout()
register_callbacks(app)


if __name__ == '__main__':
    # debug=False disables the development debugger overlay and hot
    # reloading which are only needed during active development.
    app.run(debug=False)