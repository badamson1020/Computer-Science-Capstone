# Java to Python Translation (Enhanced Python Version)

A translation of a Java JUnit testing project (Task, Contact, and Appointment
management) into Python, following the Service-Repository layered architecture
and PEP 257 documentation conventions.

## Project Structure
- `task.py`, `contact.py`, `appointment.py` — data model classes (Repository layer)
- `task_service.py`, `contact_service.py`, `appointment_service.py` — service layer
- `exceptions.py` — custom NoSuchElementException
- `test_*.py` — unittest suites for each class

## Running Tests
```bash
python -m unittest discover .
```
