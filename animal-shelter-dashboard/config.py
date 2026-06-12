"""Shared configuration, constants, and application state for the Search and Rescue Animal Dashboard.

Centralizing shared state here follows the Model-View-Controller pattern. config provides
constants and database connection that both the layout and callbacks layers can import
without creating circular dependencies between those modules.
"""

import atexit
import os

from models.shelter_crud import ShelterCRUD


###########################
# Database Connection
###########################


# Instantiate the ShelterCRUD module to handle all MongoDB communication.
# Database credentials are stored in a private .env file excluded from version
# control, preventing exposure of sensitive credentials in public repositories.
shelter = ShelterCRUD()

# Register shelter connection cleanup on application shutdown.
# Ensures MongoDB resources are freed when the Dash server stops.
atexit.register(shelter.close)


###########################
# Constants
###########################


# Retrieve all distinct breed and sex values from the database at startup.
# Populating dropdowns dynamically ensures options always reflect current data
# without requiring hardcoded lists that could become outdated.
BREEDS = sorted([b for b in shelter.read_distinct("breed", {"animal_type": "Dog"})
                if b and isinstance(b, str)])

SEX_OPTIONS = sorted([s for s in shelter.read_distinct("sex_upon_outcome", {"animal_type": "Dog"})
                      if s and isinstance(s, str)])

# Validate preset breed lists against breeds that actually exist in the database.
# Filters out any breeds not present in the current dataset to prevent the dropdown
# from displaying a misleading selected count when preset breeds do not match
# any records, e.g. showing "3 selected" but only 1 visible tag.
# If new records are imported with previously missing breeds they appear automatically.
WATER_RESCUE_BREEDS = [b for b in [
    "Labrador Retriever Mix", "Labrador Retriever",
    "Chesapeake Bay Retriever", "Chesa Bay Retr Mix", "Chesa Bay Retr",
    "Newfoundland", "Newfoundland Mix", "Golden Retriever"
] if b in BREEDS]

MOUNTAIN_RESCUE_BREEDS = [b for b in [
    "German Shepherd", "Alaskan Malamute", "Old English Sheepdog",
    "Siberian Husky", "Rottweiler"
] if b in BREEDS]

DISASTER_RESCUE_BREEDS = [b for b in [
    "Doberman Pinsch", "Doberman Pinscher", "German Shepherd",
    "Golden Retriever", "Bloodhound", "Rottweiler"
] if b in BREEDS]

# Rescue type criteria combining filter and weight settings into one constant per rescue type.
# Defined separately per rescue type rather than as a shared constant to allow
# independent adjustment if domain requirements diverge in the future.
# Weights reflect domain knowledge about rescue dog selection priorities.
# Breed is the strongest predictor of aptitude, age determines career length,
# sex is a secondary consideration.
WATER_RESCUE = {
    "breeds": WATER_RESCUE_BREEDS,
    "sex": "Intact Female",
    "age_min": 26,
    "age_max": 156,
    "breed_weight": 50,
    "sex_weight": 20,
    "age_weight": 30
}

MOUNTAIN_RESCUE = {
    "breeds": MOUNTAIN_RESCUE_BREEDS,
    "sex": "Intact Male",
    "age_min": 26,
    "age_max": 156,
    "breed_weight": 50,
    "sex_weight": 20,
    "age_weight": 30
}

DISASTER_RESCUE = {
    "breeds": DISASTER_RESCUE_BREEDS,
    "sex": "Intact Male",
    "age_min": 20,
    "age_max": 300,
    "breed_weight": 50,
    "sex_weight": 20,
    "age_weight": 30
}

# Grazioso Salvare exclusively trains dogs for search and rescue operations.
# Defined as a constant to allow easy updates if the organization expands to other animal types.
ALL_DATA_TABLE_FILTER = {"animal_type": "Dog"}

# When All is selected the pie chart shows only rescue-relevant breeds rather than all shelter breeds.
# Displaying all breeds would produce hundreds of tiny slices with no actionable insight for the organization.
ALL_PIE_CHART_FILTER = {"breed": {"$in": [
    "Labrador Retriever Mix", "Labrador Retriever",
    "Chesapeake Bay Retriever", "Chesa Bay Retr", "Chesa Bay Retr Mix",
    "Newfoundland", "Newfoundland Mix", "Golden Retriever",
    "German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky",
    "Doberman Pinsch", "Doberman Pinscher", "Bloodhound", "Rottweiler"
]}}

# Minimum percentage threshold for pie chart breed slices.
# Breeds below this threshold are grouped into an "Other" category
# to prevent the chart from becoming unreadable with too many small slices.
PIE_CHART_THRESHOLD = 0.02

# Default map center coordinates for Austin, Texas where the shelter is located
DEFAULT_LAT = 30.75
DEFAULT_LON = -97.48

# Statistics panel refresh interval in milliseconds.
# Refreshes every 5 minutes to reflect any database changes made by admins
# without requiring a manual page reload. A timed interval is used rather than
# reacting to individual database operations because the dashboard currently has
# no create, update, or delete UI. For production environments requiring immediate
# refresh on database changes, MongoDB change streams combined with a WebSocket
# connection would provide real-time updates.
STATS_REFRESH_INTERVAL = 300000  # 5 minutes in milliseconds

# MongoDB aggregation pipeline for the shelter statistics panel.
# Uses a $match stage at the pipeline level to filter for dog records once
# before branching into the $facet stage. This is more efficient than
# repeating the animal_type filter inside each individual facet.
#
# The $facet stage runs five calculations simultaneously in a single database
# call, minimizing round trips to MongoDB. Performing this processing at the
# database level rather than retrieving raw records and processing in Python
# is more efficient and scalable for large collections.
#
# The five facets run in parallel:
#   waterRescueCount    - dogs matching full Water Rescue criteria (breed, sex, age)
#   mountainRescueCount - dogs matching full Mountain Rescue criteria (breed, sex, age)
#   disasterRescueCount - dogs matching full Disaster Rescue criteria (breed, sex, age)
#   topThreeBreeds      - top 3 most common dog breeds by record count
#   averageAge          - average age of all dogs in weeks rounded to nearest whole number
#
# Full rescue filter criteria are applied to each rescue count facet rather than
# breed only, to reflect realistic candidate counts that match what the weighted
# search algorithm would return for each rescue type.
STATS_PIPELINE = [
    {"$match": {"animal_type": "Dog"}},
    {
        "$facet": {
            "waterRescueCount": [
                {"$match": {
                    "breed": {"$in": WATER_RESCUE_BREEDS},
                    "sex_upon_outcome": WATER_RESCUE["sex"],
                    "age_upon_outcome_in_weeks": {
                        "$gte": WATER_RESCUE["age_min"],
                        "$lte": WATER_RESCUE["age_max"]
                    }
                }},
                {"$count": "total"}
            ],
            "mountainRescueCount": [
                {"$match": {
                    "breed": {"$in": MOUNTAIN_RESCUE_BREEDS},
                    "sex_upon_outcome": MOUNTAIN_RESCUE["sex"],
                    "age_upon_outcome_in_weeks": {
                        "$gte": MOUNTAIN_RESCUE["age_min"],
                        "$lte": MOUNTAIN_RESCUE["age_max"]
                    }
                }},
                {"$count": "total"}
            ],
            "disasterRescueCount": [
                {"$match": {
                    "breed": {"$in": DISASTER_RESCUE_BREEDS},
                    "sex_upon_outcome": DISASTER_RESCUE["sex"],
                    "age_upon_outcome_in_weeks": {
                        "$gte": DISASTER_RESCUE["age_min"],
                        "$lte": DISASTER_RESCUE["age_max"]
                    }
                }},
                {"$count": "total"}
            ],
            "topThreeBreeds": [
                {"$group": {"_id": "$breed", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 3}
            ],
            "averageAge": [
                {"$group": {
                    "_id": None,
                    "avgAge": {"$avg": "$age_upon_outcome_in_weeks"}
                }}
            ]
        }
    }
]


###########################
# Logo Configuration
###########################


# Check for logo file at startup and warn if missing rather than crashing.
# Dash serves files from the assets folder automatically so no encoding is needed,
# but we verify the file exists to provide a clear error message if it is missing.
LOGO_PATH = '/assets/Grazioso_Salvare_Logo.png'
LOGO_EXISTS = os.path.exists('assets/Grazioso_Salvare_Logo.png')

if not LOGO_EXISTS:
    print("Warning: Logo image file not found in assets folder.")