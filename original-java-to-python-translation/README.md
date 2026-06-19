# Task Management System (Original Java Version)

This folder contains the original Java implementation of the task management system, built for CS 320: Software Testing, Automation, and Quality Assurance. It is preserved here for comparison against the Python translation in `enhanced-java-to-python-translation/`, which was built for the CS 499 capstone.

## Files

- `Task.java`, `Contact.java`, `Appointment.java` &mdash; data model classes enforcing field-level validation
- `TaskService.java`, `ContactService.java`, `AppointmentService.java` &mdash; service classes managing collections of model objects and enforcing business rules
- `TaskTest.java`, `ContactTest.java`, `AppointmentTest.java` &mdash; JUnit tests for the data model classes
- `TaskServiceTest.java`, `ContactServiceTest.java`, `AppointmentServiceTest.java` &mdash; JUnit tests for the service classes

## Architecture

This project follows a Service-Repository layered architecture. The model classes form the data layer, enforcing field-level validation rules such as ID length and required fields. The service classes form the service layer, managing collections of model objects and enforcing collection-level business rules such as preventing duplicate IDs.

## A Note on Running This Version

This project was built in Eclipse using JUnit 5, added directly as an 
Eclipse-managed library rather than through a build tool like Maven or 
Gradle. It targets Java 23. The project also references Lombok as an 
external library, though its usage was inconsistent across the original 
codebase, only some files used the `@EqualsAndHashCode` annotation it 
provides, which was one of the inconsistencies addressed in the Python 
translation. To run this version, import the files into a new Eclipse 
project and ensure JUnit 5 is available on the build path.

## What Changed

The Python translation in `enhanced-java-to-python-translation/` preserves this original Service-Repository architecture while addressing several inconsistencies in the original implementation. Defensive copying, which only existed for the `Appointment` class in this version, was implemented consistently across all three model and service class pairs. A custom `NoSuchElementException` was created in Python to mirror the original Java exception, since Python has no direct built-in equivalent. Repeated code in the service classes was consolidated into private helper methods, and all files were updated with PEP 257 compliant documentation explaining not just what the code does but why specific design decisions were made. A detailed explanation of these changes is available in the enhancement narrative on my [ePortfolio](https://badamson1020.github.io/Computer-Science-Capstone/).
