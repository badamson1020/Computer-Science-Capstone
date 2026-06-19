# Animal Shelter Dashboard

A Dash web application for Grazioso Salvare to search and rank shelter dogs
for search-and-rescue training candidacy, built on a MongoDB backend.

## Features

- Weighted multi-criteria matching algorithm (breed, sex, age) that scores
  dogs from 0 to 100 rather than using a binary filter
- Live shelter statistics panel powered by a MongoDB aggregation pipeline,
  refreshing automatically on an interval
- Interactive data table, breed distribution pie chart, and geolocation map
- Production-style MVC architecture separating layout, callbacks, and data access

## Project Structure

```
enhanced-animal-shelter-dashboard/
├── app.py                  # Entry point
├── config.py                # Shared constants, database connection, aggregation pipeline
├── layout.py                 # Dashboard layout (View)
├── callbacks.py                # Interactivity and data flow (Controller)
├── models/
│   ├── shelter_crud.py          # MongoDB data access (CRUD + aggregate)
│   └── algorithm.py               # Weighted matching algorithm
├── tests/
│   ├── test_crud.py
│   └── test_algorithm.py
├── data/
│   └── aac_shelter_outcomes.csv     # Sample shelter dataset
├── assets/
│   └── Grazioso_Salvare_Logo.png
├── .env.example                  # Template for production database credentials
├── .env.test.example                # Template for test database credentials
└── requirements.txt
```

## Prerequisites

- Python 3.10 or later
- MongoDB Community Server (running locally) and MongoDB Compass (optional, for managing data visually)

## Running Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create MongoDB databases and a user

This project expects two databases: `AAC` for production data and `AAC_Test`
for running the test suite without touching production data.

Open MongoDB Compass (or `mongosh`) and connect to your local MongoDB instance.
Using the embedded MongoSH tab in Compass, or a terminal with `mongosh`, run:

```javascript
// Create the production database user
use AAC
db.createUser({
  user: "aacuser",
  pwd: "choose_a_strong_password",
  roles: [{ role: "readWrite", db: "AAC" }]
})

// Create the test database user
use AAC_Test
db.createUser({
  user: "aacuser",
  pwd: "choose_a_different_strong_password",
  roles: [{ role: "readWrite", db: "AAC_Test" }]
})
```

Using two different passwords for the production and test users is recommended,
so that if one credential is ever exposed the other database is unaffected.

### 3. Import the sample dataset

Use MongoDB Compass's import wizard, which allows column types to be set
before the import completes:

1. In Compass, navigate to the `AAC` database and create (or open) the `animals` collection.
2. Click **Import Data**, select `data/aac_shelter_outcomes.csv`, and choose **CSV** as the input file type.
3. On the field preview screen, set the following column types before importing:

   | Field | Type |
   |---|---|
   | `rec_num` | Int32 |
   | `date_of_birth` | Date |
   | `location_lat` | Double |
   | `location_long` | Double |
   | `age_upon_outcome_in_weeks` | Double |

   All other fields (`animal_id`, `animal_type`, `breed`, `color`, `datetime`,
   `monthyear`, `name`, `outcome_subtype`, `outcome_type`, `sex_upon_outcome`,
   `age_upon_outcome`) should remain as **String**.

4. Complete the import, then repeat the same process for the `AAC_Test` database.

### 4. Configure environment variables

The application reads connection settings from `.env` and `.env.test`, which
are excluded from version control since they contain credentials. Copy the
provided example files and rename them, then fill in the values you chose above:

```bash
# macOS / Linux / Git Bash
cp .env.example .env
cp .env.test.example .env.test

# Windows PowerShell
copy .env.example .env
copy .env.test.example .env.test
```

Edit `.env` and `.env.test` with the username, password, host, port, and
database names matching what you configured in step 2.

### 5. Run the app

```bash
python app.py
```

Visit `http://127.0.0.1:8050` in your browser.

### 6. Run tests

Tests run against the `AAC_Test` database configured in `.env.test`, so the
production `AAC` database is never modified during testing.

```bash
python -m unittest discover tests
```

## Architecture Notes

The application follows a Model-View-Controller pattern:

- **Model** — `models/shelter_crud.py` (data access) and `models/algorithm.py` (business logic)
- **View** — `layout.py`, defining the dashboard's structure and components
- **Controller** — `callbacks.py`, handling interactivity and coordinating between the model and view

`config.py` holds shared constants, the database connection, and the aggregation
pipeline definition used by the statistics panel, and is imported by both
`layout.py` and `callbacks.py` to avoid circular imports.
