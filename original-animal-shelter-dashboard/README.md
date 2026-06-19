# Animal Shelter Dashboard (Original)

This folder contains the original, pre-enhancement version of the animal shelter dashboard, built for CS 340: Client/Server Development. It is preserved here for comparison against the enhanced version in `enhanced-animal-shelter-dashboard/`, which was built for the CS 499 capstone.

## Files

- `crud_module.py` &mdash; the original CRUD module for interacting with MongoDB
- `test_script.ipynb` &mdash; an informal, print-based test script for the CRUD module
- `animal_shelter_dashboard.ipynb` &mdash; the original Jupyter Dash dashboard, including the search filter, data table, pie chart, and geolocation map

## A Note on Running This Version

This version is not runnable as-is. It depends on `JupyterDash`, which is largely deprecated, and the CRUD module has database credentials hardcoded directly in the source rather than loaded from an environment file. Both of these issues were specifically addressed in the enhanced version.

The original dataset and shelter logo are not duplicated in this folder since they are unchanged between versions. They can be found in `enhanced-animal-shelter-dashboard/data/aac_shelter_outcomes.csv` and `enhanced-animal-shelter-dashboard/assets/Grazioso_Salvare_Logo.png`.

## What Changed

The enhanced version converted this project from a Jupyter notebook into a standalone Dash application, moved credentials to a private configuration file, replaced the binary search filter with a weighted multi-criteria matching algorithm, added a MongoDB aggregation pipeline for live shelter statistics, restructured the application into a multi-file MVC architecture, and replaced the print-based test script with a full unittest suite. A detailed explanation of these changes is available in the enhancement narratives on my [ePortfolio](https://badamson1020.github.io/Computer-Science-Capstone/).
