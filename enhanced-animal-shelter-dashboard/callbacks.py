"""Callback definitions for the Search and Rescue Animal Dashboard.

Following the Model-View-Controller pattern this module is the Controller layer,
responsible for handling user interactions and coordinating between the
data layer (config, shelter_crud, algorithm) and the view layer (layout).
"""

import math

import dash_leaflet as dl
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html
from dash.dependencies import Input, Output, State

from config import (shelter, ALL_DATA_TABLE_FILTER, ALL_PIE_CHART_FILTER,
                    PIE_CHART_THRESHOLD, WATER_RESCUE, MOUNTAIN_RESCUE,
                    DISASTER_RESCUE, DEFAULT_LAT, DEFAULT_LON, STATS_PIPELINE)
from models.algorithm import get_scored_results


def register_callbacks(app) -> None:
    """Register all dashboard callbacks with the Dash application instance.

    Accepting the app instance as a parameter rather than importing it directly
    prevents circular imports between app.py, layout.py, and callbacks.py.

    Args:
        app: The Dash application instance.
    """

    @app.callback(
        Output('search-panel', 'style'),
        [Input('filter-dropdown', 'value')]
    )
    def toggle_search_panel(filter_value: str) -> dict:
        """Show or hide the extended search panel based on the dropdown selection.

        The panel is hidden when All is selected since no weighted criteria are needed.
        For all other selections the panel is displayed to allow weighted search input.

        Args:
            filter_value: The selected dropdown option.

        Returns:
            Style dictionary showing or hiding the search panel.
        """
        if filter_value == 'All':
            return {'display': 'none'}
        else:
            return {'display': 'block'}

    @app.callback(
        [Output('breed-select', 'value'),
         Output('sex-select', 'value'),
         Output('age-min', 'value'),
         Output('age-max', 'value'),
         Output('breed-weight', 'value'),
         Output('sex-weight', 'value'),
         Output('age-weight', 'value')],
        [Input('filter-dropdown', 'value')]
    )
    def populate_search_fields(filter_value: str) -> tuple:
        """Auto-populate the extended search fields when a preset rescue type is selected.

        Custom and All selections clear all fields so the user can start from scratch.
        Default weights reflect domain knowledge about rescue dog selection priorities:
        breed weight 50, age weight 30, sex weight 20.

        Args:
            filter_value: The selected dropdown option.

        Returns:
            Tuple of values for all search input fields.
        """
        if filter_value == 'Water Rescue':
            return (
                WATER_RESCUE["breeds"],
                [WATER_RESCUE["sex"]],
                WATER_RESCUE["age_min"],
                WATER_RESCUE["age_max"],
                WATER_RESCUE["breed_weight"],
                WATER_RESCUE["sex_weight"],
                WATER_RESCUE["age_weight"]
            )
        elif filter_value == 'Mountain/Wilderness Rescue':
            return (
                MOUNTAIN_RESCUE["breeds"],
                [MOUNTAIN_RESCUE["sex"]],
                MOUNTAIN_RESCUE["age_min"],
                MOUNTAIN_RESCUE["age_max"],
                MOUNTAIN_RESCUE["breed_weight"],
                MOUNTAIN_RESCUE["sex_weight"],
                MOUNTAIN_RESCUE["age_weight"]
            )
        elif filter_value == 'Disaster Rescue/Individual Tracking':
            return (
                DISASTER_RESCUE["breeds"],
                [DISASTER_RESCUE["sex"]],
                DISASTER_RESCUE["age_min"],
                DISASTER_RESCUE["age_max"],
                DISASTER_RESCUE["breed_weight"],
                DISASTER_RESCUE["sex_weight"],
                DISASTER_RESCUE["age_weight"]
            )
        else:
            # Custom or All: clear all fields
            return None, None, None, None, 0, 0, 0

    # allow_duplicate=True is required on the weight value outputs because
    # populate_search_fields also writes to these same components when a preset
    # is selected. Dash normally forbids multiple callbacks writing to the same
    # output to prevent unpredictable behavior, but here it is safe because
    # the two callbacks are triggered by completely different inputs and cannot
    # fire simultaneously. populate_search_fields fires when the dropdown changes,
    # toggle_weights fires when the criteria fields change. There is no scenario
    # where both run at the same time, so the duplicate outputs do not conflict.
    # prevent_initial_call=True is also required when using allow_duplicate=True
    # to prevent toggle_weights from firing on page load before the user has
    # interacted with anything.
    # allow_duplicate=True is required here but not on populate_search_fields
    # because populate_search_fields was the first callback to declare these
    # outputs. Dash assigns ownership to the first declaration by default.
    @app.callback(
        [Output('breed-weight', 'disabled'),
         Output('sex-weight', 'disabled'),
         Output('age-weight', 'disabled'),
         Output('breed-weight', 'value', allow_duplicate=True),
         Output('sex-weight', 'value', allow_duplicate=True),
         Output('age-weight', 'value', allow_duplicate=True),
         Output('breed-weight-note', 'children'),
         Output('sex-weight-note', 'children'),
         Output('age-weight-note', 'children')],
        [Input('breed-select', 'value'),
         Input('sex-select', 'value'),
         Input('age-min', 'value'),
         Input('age-max', 'value')],
        [State('breed-weight', 'value'),
         State('sex-weight', 'value'),
         State('age-weight', 'value')],
        prevent_initial_call=True
    )
    def toggle_weights(breeds_selected: list | None, sex_selected: list | None,
                       age_min: float | None, age_max: float | None,
                       breed_weight: float | None, sex_weight: float | None,
                       age_weight: float | None) -> tuple:
        """Disable weight inputs for criteria fields that have no selection.

        Resets disabled weight values to zero to prevent them from contributing
        to the total, ensuring the remainder display is accurate.
        When a criterion is empty its weight is locked to 0 and a note is displayed
        explaining that a selection must be made to enable the weight input.

        Args:
            breeds_selected: Selected breed values.
            sex_selected: Selected sex values.
            age_min: Minimum age value.
            age_max: Maximum age value.
            breed_weight: Current breed weight value.
            sex_weight: Current sex weight value.
            age_weight: Current age weight value.

        Returns:
            Tuple of disabled states, reset values, and note text for each weight input.
        """
        note = "Select a preference to enable"

        breed_disabled = not bool(breeds_selected)
        sex_disabled = not bool(sex_selected)
        age_disabled = not bool(age_min is not None and age_max is not None)

        # Reset value to 0 if disabled, otherwise keep the current value.
        # State is used for weight values rather than Input to avoid a circular
        # dependency. The callback reads current values without reacting to them changing.
        new_breed_weight = 0 if breed_disabled else (breed_weight or 0)
        new_sex_weight = 0 if sex_disabled else (sex_weight or 0)
        new_age_weight = 0 if age_disabled else (age_weight or 0)

        breed_note = note if breed_disabled else ""
        sex_note = note if sex_disabled else ""
        age_note = note if age_disabled else ""

        return (breed_disabled, sex_disabled, age_disabled,
                new_breed_weight, new_sex_weight, new_age_weight,
                breed_note, sex_note, age_note)

    @app.callback(
        [Output('weight-remaining', 'children'),
         Output('weight-remaining', 'style'),
         Output('search-button', 'disabled'),
         Output('age-validation-msg', 'children'),
         Output('search-validation-msg', 'children')],
        [Input('breed-weight', 'value'),
         Input('sex-weight', 'value'),
         Input('age-weight', 'value'),
         Input('age-min', 'value'),
         Input('age-max', 'value'),
         Input('breed-select', 'value'),
         Input('sex-select', 'value')]
    )
    def update_validation(breed_weight: float | None, sex_weight: float | None,
                          age_weight: float | None, age_min: float | None,
                          age_max: float | None, breeds_selected: list | None,
                          sex_selected: list | None) -> tuple:
        """Update the weight remainder display and validate all inputs in real time.

        The Search button remains disabled until all validation passes.
        Age validation is displayed inline next to the age inputs.
        Weight validation is displayed next to the search button.
        Provides specific error messages for each validation failure so users
        know exactly what needs to be corrected before searching.

        Args:
            breed_weight: Weight assigned to the breed criterion.
            sex_weight: Weight assigned to the sex criterion.
            age_weight: Weight assigned to the age criterion.
            age_min: Minimum age value entered by the user.
            age_max: Maximum age value entered by the user.
            breeds_selected: Selected breed values from the breed dropdown.
            sex_selected: Selected sex values from the sex dropdown.

        Returns:
            Tuple of remaining display text, style, button disabled state, and error messages.
        """
        bw = breed_weight or 0
        sw = sex_weight or 0
        aw = age_weight or 0
        total = bw + sw + aw
        remaining = 100 - total

        # At least one criterion must be selected
        no_criteria = not breeds_selected and not sex_selected and (age_min is None and age_max is None)

        # Check for decimal weight values: weights must be whole numbers
        # prevents fragile floating point comparisons elsewhere
        weights_are_integers = all(
            w is None or w == int(w)
            for w in [breed_weight, sex_weight, age_weight]
        )

        # Check for decimal age values: age in weeks should be a whole number
        # to avoid floating point precision issues in boundary comparisons
        ages_are_integers = all(
            a is None or a == int(a)
            for a in [age_min, age_max]
        )

        # Check if only one age value is provided
        age_partial = (age_min is not None) != (age_max is not None)

        # Age validation section
        # Displayed inline next to the age inputs
        age_msg = ""
        age_invalid = False

        if not ages_are_integers:
            age_msg = "Age values must be whole numbers. Decimal values are not allowed"
            age_invalid = True
        elif age_partial:
            age_msg = "Please enter both a minimum and maximum age"
            age_invalid = True
        elif age_min is not None and age_max is not None and age_min >= age_max:
            age_msg = "Minimum age must be less than maximum age"
            age_invalid = True

        # Remaining display section
        if remaining > 0:
            remaining_text = f"Remaining: {remaining}"
            remaining_style = {'fontWeight': 'bold', 'marginBottom': '15px', 'color': 'black'}
        elif remaining == 0:
            remaining_text = "Remaining: 0 ✓"
            remaining_style = {'fontWeight': 'bold', 'marginBottom': '15px', 'color': 'green'}
        else:
            remaining_text = f"{remaining} ({abs(remaining)} over limit)"
            remaining_style = {'fontWeight': 'bold', 'marginBottom': '15px', 'color': 'red'}

        # Weight / search validation section
        # Displayed next to the search button
        search_msg = ""
        button_disabled = True

        if no_criteria:
            search_msg = "Please select at least one search criterion"
        elif not weights_are_integers:
            search_msg = "Weights must be whole numbers. Decimal values are not allowed"
        elif age_invalid:
            search_msg = "Please fix the age range before searching"
        elif remaining != 0:
            search_msg = f"Weights must sum to 100. Current total: {total}"
        else:
            button_disabled = False

        return remaining_text, remaining_style, button_disabled, age_msg, search_msg

    @app.callback(
        [Output('datatable-id', 'data'),
         Output('datatable-id', 'page_current')],
        [Input('filter-dropdown', 'value'),
         Input('search-button', 'n_clicks')],
        [State('breed-select', 'value'),
         State('sex-select', 'value'),
         State('age-min', 'value'),
         State('age-max', 'value'),
         State('breed-weight', 'value'),
         State('sex-weight', 'value'),
         State('age-weight', 'value')]
    )
    def update_table(filter_value: str, _clicked: int, breeds_selected: list | None,
                     sex_selected: list | None, age_min: float | None, age_max: float | None,
                     breed_weight: float | None, sex_weight: float | None,
                     age_weight: float | None) -> tuple[list[dict], int]:
        """Update the data table based on the selected filter or weighted search.

        For All: queries all dogs and assigns a match score of 0 since no
        weighted criteria are applied.

        For all other selections: retrieves all dogs, builds the criteria dictionary,
        and delegates scoring and filtering to get_scored_results. The match score
        is added to each record in memory and never written to MongoDB, ensuring
        the database remains unmodified by search operations.

        Both paths produce a consistent scored_data list that feeds into shared
        DataFrame building and column selection logic before being returned.
        Also resets the table to page 1 on every new search or filter change
        so results always display from the beginning.

        Args:
            filter_value: The selected dropdown option.
            _clicked: Unused. Search button click triggers the callback but the
                      click count is not needed inside the function.
            breeds_selected: Selected breed values.
            sex_selected: Selected sex values.
            age_min: Minimum age in weeks.
            age_max: Maximum age in weeks.
            breed_weight: Weight assigned to breed criterion.
            sex_weight: Weight assigned to sex criterion.
            age_weight: Weight assigned to age criterion.

        Returns:
            Tuple of matching records sorted by match score descending and page reset to 0.
        """
        try:
            if filter_value == 'All':
                # Simple query, no weighted scoring applied.
                # match_score set to 0.0 for all records to maintain consistent
                # data structure with the weighted search path below.
                data = shelter.read(ALL_DATA_TABLE_FILTER)
                scored_data = [dict(dog, match_score=0.0) for dog in data]
            else:
                # Weighted search: retrieve all dogs and delegate scoring to get_scored_results.
                # All dogs are retrieved rather than pre-filtering in MongoDB because
                # the weighted algorithm scores partial matches that a strict query would exclude.
                data = shelter.read(ALL_DATA_TABLE_FILTER)
                criteria = {
                    "breeds": breeds_selected or [],
                    "sex": sex_selected or [],
                    "age_min": age_min,
                    "age_max": age_max,
                    "breed_weight": breed_weight or 0,
                    "sex_weight": sex_weight or 0,
                    "age_weight": age_weight or 0
                }
                scored_data = get_scored_results(data, criteria)

            if not scored_data:
                return [], 0

            # Build DataFrame from scored results, drop MongoDB internal _id field,
            # and select only the columns needed for display in the DataTable.
            df = pd.DataFrame(scored_data)
            if '_id' in df.columns:
                df.drop(columns=['_id'], inplace=True)
            # Only select columns that exist in the DataFrame
            available_cols = [c for c in ['match_score', 'animal_id', 'breed', 'name',
                                          'age_upon_outcome_in_weeks', 'sex_upon_outcome',
                                          'location_lat', 'location_long', 'outcome_type']
                              if c in df.columns]
            df = df[available_cols]
            return df.to_dict('records'), 0

        except Exception as e:
            print("An error occurred while attempting to load the data:", e)
            return [], 0

    @app.callback(
        Output('datatable-id', 'selected_rows'),
        [Input('datatable-id', 'page_current'),
         Input('filter-dropdown', 'value'),
         Input('search-button', 'n_clicks')]
    )
    def reset_selected_rows(_page_current: int, _filter_value: str, _clicked: int) -> list:
        """Reset the selected row when the data set changes.

        Fires when the user navigates to a new page, changes the filter dropdown,
        or clicks the search button. Prevents the map from displaying a stale
        selection when the underlying data set changes.

        Args:
            _page_current: Unused. Page navigation triggers the callback but the
                           page number is not needed inside the function.
            _filter_value: Unused. Filter change triggers the callback but the
                           selected value is not needed inside the function.
            _clicked: Unused. Search button click triggers the callback but the
                      click count is not needed inside the function.

        Returns:
            Empty list clearing any existing row selection.
        """
        return []

    @app.callback(
        Output('map-id', "children"),
        [Input('datatable-id', "derived_virtual_data"),
         Input('datatable-id', "derived_virtual_selected_rows")]
    )
    def update_map(view_data: list[dict] | None, selected_row: list[int] | None) -> dl.Map:
        """Update the geolocation map when a row is selected in the data table.

        Centers the map on the selected dog's coordinates and displays a marker
        with a popup showing breed, age, sex, and name details.
        Defaults to Austin, Texas when no row is selected since that is where
        the shelter is located.

        Args:
            view_data: The current visible rows in the data table.
            selected_row: Index of the currently selected row.

        Returns:
            Leaflet map component centered on the selected dog or Austin TX.
        """
        try:
            if not selected_row or view_data is None:
                return dl.Map(
                    dl.TileLayer(),
                    center=[DEFAULT_LAT, DEFAULT_LON],
                    zoom=6,
                    style={'height': '500px'}
                )
            else:
                dff = view_data[selected_row[0]]
                lat = dff.get('location_lat', DEFAULT_LAT)
                lon = dff.get('location_long', DEFAULT_LON)

                return dl.Map(
                    [
                        dl.TileLayer(),
                        dl.Marker(
                            position=[lat, lon],
                            children=[
                                dl.Tooltip(dff['breed']),
                                dl.Popup([
                                    html.H4(f"Breed: {dff['breed']}"),
                                    html.P(f"Age in Weeks: {round(dff['age_upon_outcome_in_weeks'], 2)}"),
                                    html.P(f"Sex: {dff['sex_upon_outcome']}"),
                                    html.P(f"Name: {dff['name']}")
                                ])
                            ]
                        )
                    ],
                    # Unique id forces component remount on selection change,
                    # ensuring the previous marker is cleared when a new dog is selected.
                    id=f"map-{lat}-{lon}",
                    center=[lat, lon],
                    zoom=10,
                    style={'height': '500px'}
                )
        except Exception as e:
            print("An error occurred while updating the map:", e)
            return dl.Map(
                dl.TileLayer(),
                center=[DEFAULT_LAT, DEFAULT_LON],
                zoom=6,
                style={'height': '500px'}
            )

    @app.callback(
        Output('pie-chart', 'figure'),
        [Input('filter-dropdown', 'value'),
         Input('datatable-id', 'data')]
    )
    def update_pie_chart(filter_value: str, table_data: list[dict] | None) -> go.Figure:
        """Update the pie chart based on the current filter selection and table data.

        For All: queries rescue-relevant breeds independently to keep the chart readable.

        For all other selections: uses the table data directly so the pie chart always
        reflects exactly the same population shown in the data table, ensuring consistency
        between the two components regardless of what weighted criteria were applied.

        Breeds representing less than the PIE_CHART_THRESHOLD percentage of results are
        grouped into an Other category to prevent the chart from becoming unreadable
        when weighted searches return many diverse breeds with small individual counts.

        Args:
            filter_value: The selected dropdown option.
            table_data: Current data in the data table from the weighted search.

        Returns:
            Plotly pie chart figure showing breed distribution.
        """
        try:
            if filter_value == 'All':
                # Independent query for rescue relevant breeds when All is selected.
                data = shelter.read(ALL_PIE_CHART_FILTER)
                df = pd.DataFrame(data)
            else:
                # Use table data directly for all other selections. Guaranteed consistency
                # with what the user sees in the data table.
                df = pd.DataFrame(table_data) if table_data else pd.DataFrame()

            if df.empty or 'breed' not in df.columns:
                return px.pie(values=[1], names=['No Data'], title="No Data Available")

            # Group breeds below the percentage threshold into an "Other" category
            # to prevent the chart from becoming unreadable with too many small slices.
            # A 2% threshold means a breed must represent at least 2% of results to
            # get its own slice, smaller breeds are grouped into Other.
            breed_counts = df['breed'].value_counts()
            # math.ceil eliminates the possible floating point comparison in the next line.
            threshold = math.ceil(len(df) * PIE_CHART_THRESHOLD)
            major_breeds = breed_counts[breed_counts >= threshold].reset_index()
            major_breeds.columns = ['breed', 'count']

            other_count = breed_counts[breed_counts < threshold].sum()
            if other_count > 0:
                other_row = pd.DataFrame([{'breed': 'Other', 'count': other_count}])
                major_breeds = pd.concat([major_breeds, other_row], ignore_index=True)

            # Title reflects what the chart is actually showing rather than the filter name.
            # All shows rescue relevant breeds so the title reflects that specifically.
            # All other selections show search result breeds so the title reflects that.
            title = ("Rescue Relevant Breed Distribution" if filter_value == 'All'
                     else "Search Results Breed Distribution")

            fig = px.pie(major_breeds, values='count', names='breed',
                         title=title, height=800, width=800)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(title_x=0.5)
            return fig

        except Exception as e:
            print("An error occurred while updating the pie chart:", e)
            return px.pie(values=[1], names=['Error'], title="Error Loading Chart")

    @app.callback(
        [Output('stats-water', 'children'),
         Output('stats-mountain', 'children'),
         Output('stats-disaster', 'children'),
         Output('stats-breed-1', 'children'),
         Output('stats-breed-2', 'children'),
         Output('stats-breed-3', 'children'),
         Output('stats-avg-age', 'children')],
        [Input('stats-refresh-interval', 'n_intervals')]
    )
    def update_stats_panel(_n_intervals: int) -> tuple:
        """Populate the shelter overview statistics panel using a MongoDB aggregation pipeline.

        Runs on startup and refreshes every STATS_REFRESH_INTERVAL milliseconds to reflect
        any database changes made by admins without requiring a page reload.

        Returns plain string values to named span components defined in layout.py.
        All HTML structure and styling lives in the layout, keeping this callback
        focused purely on data retrieval and extraction.

        The statistics panel is intentionally independent of user search inputs or filter
        selections. It always reflects the full shelter database to give users a constant
        high level overview before and during their searches.

        Data is processed at the database level via the $facet aggregation pipeline rather
        than retrieving raw records and processing in Python, which is more efficient and
        scalable for large collections.

        Args:
            _n_intervals: Number of times the interval has fired, unused beyond triggering.

        Returns:
            Tuple of seven plain string values for the statistics panel span components.
        """
        try:
            results = shelter.aggregate(STATS_PIPELINE)

            if not results:
                return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"

            data = results[0]

            # Extract rescue candidate counts from facet results.
            # Each facet returns a list with one item containing the count,
            # or an empty list if no matching documents exist.
            water_count = data["waterRescueCount"][0]["total"] if data["waterRescueCount"] else 0
            mountain_count = data["mountainRescueCount"][0]["total"] if data["mountainRescueCount"] else 0
            disaster_count = data["disasterRescueCount"][0]["total"] if data["disasterRescueCount"] else 0

            # Extract top three breeds. Each item has _id (breed name) and count.
            # Padded to always return three values even if fewer breeds exist.
            top_breeds = data.get("topThreeBreeds", [])
            breed_items = [f"{b['_id']} ({b['count']})" for b in top_breeds]
            while len(breed_items) < 3:
                breed_items.append("N/A")

            # Extract average age rounded to nearest whole number
            avg_age_data = data.get("averageAge", [])
            avg_age = round(avg_age_data[0]["avgAge"]) if avg_age_data else 0

            return (
                str(water_count),
                str(mountain_count),
                str(disaster_count),
                breed_items[0],
                breed_items[1],
                breed_items[2],
                f"{avg_age} weeks"
            )

        except Exception as e:
            print(f"An error occurred while updating the statistics panel: {e}")
            return "Error", "Error", "Error", "Error", "Error", "Error", "Error"