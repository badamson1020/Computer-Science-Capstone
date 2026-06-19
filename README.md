# Computer-Science-Capstone

This repository contains the enhanced artifacts for my CS 499 Computer Science Capstone at Southern New Hampshire University. It includes both the original, pre-enhancement versions of two source projects and the enhanced versions developed for the capstone, covering all three required categories: software design and engineering, algorithms and data structures, and databases.

View the full ePortfolio, including enhancement narratives, side-by-side code comparisons, the code review video, and my professional self-assessment, at: **[https://badamson1020.github.io/Computer-Science-Capstone/](https://badamson1020.github.io/Computer-Science-Capstone/)**

## Repository Structure

- `enhanced-animal-shelter-dashboard/` &mdash; the animal shelter dashboard after both enhancement two and enhancement three
- `enhanced-java-to-python-translation/` &mdash; the Python translation of the original Java project, enhancement one
- `original-animal-shelter-dashboard/` &mdash; the original, pre-enhancement version of the shelter dashboard
- `original-java-to-python/` &mdash; the original Java version 

## Enhancements

### Enhancement One: Software Engineering and Design
The original artifact is a Java task-management system built for CS 320: Software Testing, Automation, and Quality Assurance,
implementing task, contact, and appointment tracking through a layered 
architecture with full JUnit test coverage. For the capstone, this project 
was translated into Python while preserving and strengthening
its original Service-Repository layered architecture. The translation addressed inconsistencies in the original implementation, including incomplete defensive copying, and added PEP 257 compliant documentation throughout.

### Enhancement Two: Algorithms and Data Structures
The original artifact is a Python web dashboard built for CS 340: Client/Server Development, allowing 
a fictional search-and-rescue training organization to browse and filter 
shelter dogs by breed, sex, and age. For the capstone, the dashboard's  binary search filter, was replaced with a weighted multi-criteria matching algorithm that scores rescue dog candidates from 0 to 100 across breed, sex, and age. Building this required managing real algorithmic trade-offs, including calibrating the minimum score threshold through testing. This enhancement also addressed several security gaps, including hardcoded database credentials and inconsistent input validation.

### Enhancement Three: Databases
Building on the same animal shelter dashboard, a MongoDB aggregation pipeline was added to calculate shelter statistics directly at the database level, and the application was restructured into a production-style multi-file MVC architecture. 

Detailed narratives for each enhancement, including specific design decisions, trade-offs, and challenges, are available on my [ePortfolio](https://badamson1020.github.io/Computer-Science-Capstone/).
