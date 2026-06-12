"""Dashboard layout definition for the Search and Rescue Animal Dashboard.

Defines the visual structure and component hierarchy of the application.
Following the Model-View-Controller pattern this module is the View layer,
responsible only for describing what the user sees, not how it behaves.
All interactivity and data handling is managed in callbacks.py.
"""

from dash import dcc, html, dash_table

from config import BREEDS, SEX_OPTIONS, LOGO_PATH, LOGO_EXISTS, STATS_REFRESH_INTERVAL


def create_layout() -> html.Div:
    """Create and return the full dashboard layout as a Div component.

    Extracted into a function to allow app.py to assign it to app.layout
    after the Dash instance is created, avoiding circular import issues
    between app.py, layout.py, and callbacks.py.

    Returns:
        The complete dashboard layout as an html.Div.
    """
    return html.Div([
        html.H1("Search and Rescue Animal Dashboard", style={'textAlign': 'center'}),

        # Adds the logo to the top of the page with a hyperlink to the SNHU website.
        # Logo is conditionally rendered only if the image file was found at startup.
        html.A(
            html.Img(
                src=LOGO_PATH,
                style={'height': '110px', 'display': 'block', 'margin': '0 auto'},
                title="Visit SNHU"
            ),
            href="https://www.snhu.edu",
            target="_blank"
        ) if LOGO_EXISTS else html.Div(),

        html.H4("Created by Bethany Adamson", style={'textAlign': 'center'}),

        # Interval component for periodic statistics panel refresh.
        # Fires every STATS_REFRESH_INTERVAL milliseconds to reflect any
        # database changes made by admins without requiring a page reload.
        dcc.Interval(
            id='stats-refresh-interval',
            interval=STATS_REFRESH_INTERVAL,
            n_intervals=0
        ),

        # Shelter overview statistics panel.
        # Displays a high level summary of the full shelter database independent
        # of any user search inputs or filter selections. Loads on startup and
        # refreshes periodically so users always have current context before
        # and during their searches. Data is processed at the database level
        # via a MongoDB aggregation pipeline rather than in Python, which is
        # more efficient and scalable for large collections.
        html.Div([
            html.H5("Shelter Overview", style={
                'textAlign': 'center',
                'marginTop': '0',
                'marginBottom': '10px',
                'fontSize': '18px',
                'color': 'black'
            }),

            # Row 1: Rescue candidate counts
            html.Div([
                html.Span("Water Rescue Count: ", style={'fontWeight': 'bold', 'fontSize': '16px'}),
                html.Span(id='stats-water', style={'fontSize': '16px'}),
                html.Span("  |  ", style={'color': '#999', 'fontSize': '16px'}),
                html.Span("Mountain Rescue Count: ", style={'fontWeight': 'bold', 'fontSize': '16px'}),
                html.Span(id='stats-mountain', style={'fontSize': '16px'}),
                html.Span("  |  ", style={'color': '#999', 'fontSize': '16px'}),
                html.Span("Disaster Rescue Count: ", style={'fontWeight': 'bold', 'fontSize': '16px'}),
                html.Span(id='stats-disaster', style={'fontSize': '16px'}),
            ], style={'marginBottom': '8px', 'textAlign': 'center'}),

            # Row 2: Top three breeds
            html.Div([
                html.Span("Top Breeds: ", style={'fontWeight': 'bold', 'fontSize': '16px'}),
                html.Span(id='stats-breed-1', style={'fontSize': '16px'}),
                html.Span("  |  ", style={'color': '#999', 'fontSize': '16px'}),
                html.Span(id='stats-breed-2', style={'fontSize': '16px'}),
                html.Span("  |  ", style={'color': '#999', 'fontSize': '16px'}),
                html.Span(id='stats-breed-3', style={'fontSize': '16px'}),
            ], style={'marginBottom': '8px', 'textAlign': 'center'}),

            # Row 3: Average age
            html.Div([
                html.Span("Average Dog Age: ", style={'fontWeight': 'bold', 'fontSize': '16px'}),
                html.Span(id='stats-avg-age', style={'fontSize': '16px'}),
            ], style={'textAlign': 'center', 'marginBottom': '0'}),

        ], style={
            'width': '40%',
            'margin': '10px auto 20px auto',
            'padding': '10px 15px',
            'border': '1px solid #ddd',
            'borderRadius': '8px',
            'backgroundColor': '#f0f4f8',
        }),

        # Primary dropdown filter for selecting rescue type.
        # All hides the extended search panel and shows all dogs.
        # Preset rescue types auto-populate the extended search panel with default criteria and weights.
        # Custom opens the extended search panel with blank fields for manual entry.
        html.Div([
            html.Label("Select rescue type:", style={'fontWeight': 'bold', 'display': 'block',
                                                     'textAlign': 'left', 'width': '50%', 'margin': '0 auto'}),
            dcc.Dropdown(
                id='filter-dropdown',
                options=[
                    {'label': 'All', 'value': 'All'},
                    {'label': 'Water Rescue', 'value': 'Water Rescue'},
                    {'label': 'Mountain/Wilderness Rescue', 'value': 'Mountain/Wilderness Rescue'},
                    {'label': 'Disaster Rescue/Individual Tracking', 'value': 'Disaster Rescue/Individual Tracking'},
                    {'label': 'Custom Search', 'value': 'Custom'},
                ],
                value='All',
                clearable=False,
                style={'width': '50%', 'marginLeft': 'auto', 'marginRight': 'auto'}
            )
        ], style={'textAlign': 'center', 'paddingBottom': 20}),

        # Extended search panel: only visible when a rescue type or Custom is selected.
        # Hidden when All is selected since no weighted criteria are needed.
        # Auto-populates with preset criteria when a rescue type is selected.
        html.Div(
            id='search-panel',
            style={'display': 'none'},
            children=[
                html.Div([

                    # Search criteria section
                    html.H4("Search Criteria", style={'textAlign': 'center'}),

                    html.Div([
                        html.Label("Preferred Breeds:", style={'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            id='breed-select',
                            options=[{'label': b, 'value': b} for b in BREEDS],
                            multi=True,
                            placeholder='Search and select breeds...',
                        ),
                    ], style={'marginBottom': '15px'}),

                    html.Div([
                        html.Label("Preferred Sex:", style={'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            id='sex-select',
                            options=[{'label': s, 'value': s} for s in SEX_OPTIONS],
                            multi=True,
                            placeholder='Select preferred sex...',
                        ),
                    ], style={'marginBottom': '15px'}),

                    html.Div([
                        html.Label("Age Range (weeks):", style={'fontWeight': 'bold'}),
                        html.Div([
                            dcc.Input(
                                id='age-min',
                                type='number',
                                placeholder='Min',
                                min=0,
                                style={'width': '120px', 'marginRight': '10px'}
                            ),
                            html.Span("to", style={'marginRight': '10px'}),
                            dcc.Input(
                                id='age-max',
                                type='number',
                                placeholder='Max',
                                min=0,
                                style={'width': '120px'}
                            ),
                        ]),

                        # Age validation message, shown when min exceeds max
                        html.Div(id='age-validation-msg',
                                 style={'color': 'red', 'fontSize': '14px', 'marginTop': '5px'})
                    ], style={'marginBottom': '20px'}),

                    html.Hr(),

                    # Weight section: stacked like a math problem to make the summing requirement obvious.
                    # Weights for empty criteria fields are automatically set to 0 and disabled.
                    html.H4("Criteria Weights", style={'textAlign': 'center'}),
                    html.P(
                        "Assign importance to each criterion. Weights must sum to 100.",
                        style={'textAlign': 'center', 'fontSize': '14px', 'color': 'grey'}
                    ),

                    html.Div([
                        html.Div([
                            html.Label("Breed Weight:",
                                       style={'marginRight': '10px', 'display': 'inline-block', 'width': '120px'}),
                            dcc.Input(id='breed-weight', type='number', min=0, value=0,
                                      style={'width': '70px'}),
                            html.Span(id='breed-weight-note',
                                      style={'fontSize': '14px', 'color': 'grey', 'marginLeft': '10px',
                                             'position': 'absolute', 'whiteSpace': 'nowrap'})
                        ], style={'marginBottom': '8px', 'position': 'relative'}),

                        html.Div([
                            html.Label("Sex Weight:",
                                       style={'marginRight': '10px', 'display': 'inline-block', 'width': '120px'}),
                            dcc.Input(id='sex-weight', type='number', min=0, value=0,
                                      style={'width': '70px'}),
                            html.Span(id='sex-weight-note',
                                      style={'fontSize': '14px', 'color': 'grey', 'marginLeft': '10px',
                                             'position': 'absolute', 'whiteSpace': 'nowrap'})
                        ], style={'marginBottom': '8px', 'position': 'relative'}),

                        html.Div([
                            html.Label("Age Weight:",
                                       style={'marginRight': '10px', 'display': 'inline-block', 'width': '120px'}),
                            dcc.Input(id='age-weight', type='number', min=0, value=0,
                                      style={'width': '70px'}),
                            html.Span(id='age-weight-note',
                                      style={'fontSize': '14px', 'color': 'grey', 'marginLeft': '10px',
                                             'position': 'absolute', 'whiteSpace': 'nowrap'})
                        ], style={'marginBottom': '8px', 'position': 'relative'}),

                        html.Hr(style={'width': '210px', 'marginLeft': 'auto', 'marginRight': 'auto'}),

                        # Remaining counter: updates in real time as weights are entered.
                        # Green when exactly 0, red when over 100, neutral otherwise.
                        html.Div(id='weight-remaining', style={'fontWeight': 'bold', 'marginBottom': '15px'}),

                    ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),

                    # Search button: disabled until weights sum to 100 and inputs are valid
                    html.Div([
                        html.Button(
                            'Search',
                            id='search-button',
                            n_clicks=0,
                            disabled=True,
                            style={
                                'backgroundColor': '#4CAF50',
                                'color': 'white',
                                'padding': '10px 24px',
                                'border': 'none',
                                'borderRadius': '4px',
                                'cursor': 'pointer',
                                'fontSize': '16px'
                            }
                        ),
                        html.Div(id='search-validation-msg',
                                 style={'color': 'red', 'fontSize': '14px', 'marginTop': '5px'})
                    ], style={'textAlign': 'center', 'marginTop': '10px'})

                ], style={
                    'width': '50%',
                    'margin': '0 auto',
                    'padding': '20px',
                    'border': '1px solid #ddd',
                    'borderRadius': '8px',
                    'backgroundColor': '#f9f9f9',
                    'marginBottom': '20px'
                })
            ]
        ),

        # Data table displaying shelter dog records.
        # Supports native filtering, sorting, single row selection, and pagination.
        # Match Score column added for weighted search results, displays 0-100 percent match.
        html.Div([
            dash_table.DataTable(
                id='datatable-id',
                columns=[
                    {"name": "Match Score Percent", "id": "match_score", "deletable": False, "selectable": True,
                     "type": "numeric", "format": {"specifier": ".1f"}},
                    {"name": "Animal ID", "id": "animal_id", "deletable": False, "selectable": True},
                    {"name": "Breed", "id": "breed", "deletable": False, "selectable": True},
                    {"name": "Name", "id": "name", "deletable": False, "selectable": True},
                    {"name": "Age in Weeks", "id": "age_upon_outcome_in_weeks", "deletable": False,
                     "selectable": True, "type": "numeric", "format": {"specifier": ".2f"}},
                    {"name": "Sex", "id": "sex_upon_outcome", "deletable": False, "selectable": True},
                    {"name": "Latitude", "id": "location_lat", "deletable": False, "selectable": True,
                     "type": "numeric", "format": {"specifier": ".4f"}},
                    {"name": "Longitude", "id": "location_long", "deletable": False, "selectable": True,
                     "type": "numeric", "format": {"specifier": ".4f"}},
                    {"name": "Outcome Type", "id": "outcome_type", "deletable": False, "selectable": True},
                ],
                data=[],
                editable=False,
                row_selectable='single',
                selected_rows=[],
                sort_action="native",
                filter_action="native",
                page_action="native",
                page_current=0,
                page_size=20,
                style_table={'overflowX': 'auto'},
                style_header={
                    'backgroundColor': 'rgb(230,230,230)',
                    'fontWeight': 'bold'
                }
            )
        ], className='row'),

        html.Br(),

        # Geolocation map and pie chart displayed side by side below the data table.
        html.Div([
            html.Div(
                id='map-id',
                style={'flex': '1', 'height': '500px', 'marginRight': '10px'}
            ),
            html.Div(
                dcc.Graph(id='pie-chart'),
                style={'flex': '1.5', 'height': '800px'}
            )
        ],
        style={
            'display': 'flex',
            'flexDirection': 'row',
            'justifyContent': 'center',
            'alignItems': 'center',
            'padding': '20px'
        }),

        html.A(
            html.Img(
                src=LOGO_PATH,
                style={'height': '110px', 'display': 'block', 'margin': '0 auto'},
                title="Visit SNHU"
            ),
            href="https://www.snhu.edu",
            target="_blank"
        ) if LOGO_EXISTS else html.Div(),

        html.H4("Created by Bethany Adamson", style={'textAlign': 'center'})
    ])