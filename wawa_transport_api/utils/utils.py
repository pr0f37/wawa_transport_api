"""Module containing methods to be used across the application"""
from math import pi, sin, cos, atan2, sqrt
from typing import Dict, List


from wawa_transport_api.domain.model import BusStop, Coordinates


def parse_bus_stops(stops: List[Dict]) -> List[BusStop]:
    """
    Return a list containing a list of bus stops parsed
    from OpenApi response
    """
    return [_parse_bus_stop(stop["values"]) for stop in stops]


def _parse_bus_stop(stop: Dict) -> BusStop:
    _attrs = {val["key"]: val["value"] for val in stop}
    return BusStop(
        id=_attrs["zespol"],
        number=_attrs["slupek"],
        coords=Coordinates(
            lat=float(_attrs["szer_geo"]),
            lon=float(_attrs["dlug_geo"]),
        ),
        name=_attrs["nazwa_zespolu"],
        direction=_attrs["kierunek"],
    )


def calculate_distance(stop: BusStop, position: Coordinates) -> float:
    """
    Calculate distance between current position and a bus stop
    """
    return abs(stop.coords.lat - position.lat) + abs(stop.coords.lon - position.lon)


def calculate_haversine_distance(stop: BusStop, position: Coordinates) -> float:
    """
    Calculate distance between current position and a bus stop using haversine formulae
    Not sure if the calculation is entirely correct as the resulting distance seems to be
    way too large.
    """

    def _deg2rad(deg):
        return deg * (pi / 180)

    earth_radius = 6371
    dist_lat = _deg2rad(stop.coords.lat - position.lat)
    dist_lon = _deg2rad(stop.coords.lon - position.lon)
    a = (sin(dist_lat / 2) ** 2) + cos(_deg2rad(stop.coords.lat)) * cos(
        _deg2rad(position.lat)
    ) * (sin(dist_lon / 2) ** 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius * c


def closest_stop(
    stops: List[BusStop], position: Coordinates, distance_func=calculate_distance
) -> BusStop:
    """
    Return the closest stop from the list to the position given in second argument.
    """
    min_dist = float("inf")
    for stop in stops:
        dist = distance_func(stop=stop, position=position)
        if dist < min_dist:
            closest = stop
            min_dist = dist
    return closest
