"""Custom exceptions for the Service-Repository pattern implementation.

Provides exception classes that mirror Java's exception hierarchy for use
during the Java to Python translation. Python has no direct built-in
equivalent for some Java exceptions, so custom classes are defined here
to preserve the same semantics and exception hierarchy as the original
Java implementation.
"""


class NoSuchElementException(Exception):
    """Raise when a requested element cannot be found in a collection.

    Mirrors Java's NoSuchElementException behavior. Python has no direct
    built-in equivalent, so this custom class preserves the same exception
    hierarchy and semantics as the original Java implementation during
    translation.
    """
    pass