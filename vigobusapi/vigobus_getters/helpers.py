"""HELPERS
Helper misc functions for external data management
"""

# # Native # #
import inspect
import datetime

# # Project # #
from vigobusapi.entities import Stop, Buses

__all__ = ("get_package", "add_stop_created_timestamp", "sort_buses")


def get_package(function) -> str:
    """Return the package name from the given object (usually a function).
    Only return the last package (inmediate first parent of the object).
    """
    return inspect.getmodule(function).__name__.split(".")[-1]


def add_stop_created_timestamp(stop: Stop) -> Stop:
    """Add the 'created' field to the given Stop object, with the current datetime timestamp.
    The timestamp is created as a datetime object in the current local time and timezone.
    The input object is modified in-place. The same object is returned.
    """
    utc_dt = datetime.datetime.now(datetime.timezone.utc)  # UTC time
    local_dt = utc_dt.astimezone()  # local time
    stop.created = local_dt
    return stop


def sort_buses(buses: Buses):
    """Sort an array of Buses by time and route. The array is sorted in-place (nothing is returned)"""
    buses.sort(key=lambda bus: (bus.time, bus.route))
