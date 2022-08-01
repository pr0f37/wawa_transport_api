"""Module containing methods to be used across the application"""
from math import atan2, cos, pi, sin, sqrt
from typing import Dict, List
from datetime import time, datetime

from wawa_transport_api.domain.model import (
    BusStop,
    Coordinates,
    Line,
    Timeline,
    Timetable,
)


def parse_stops(stops: List[Dict]) -> List[BusStop]:
    """
    Return a list containing parsed bus stops from OpenApi response
    """
    return [_parse_stop(stop["values"]) for stop in stops]


def _parse_stop(stop: List[Dict]) -> BusStop:
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


def _parse_line(line: Dict) -> Line:
    _attrs = {val["key"]: val["value"] for val in line}
    return Line(number=_attrs["linia"])


def parse_lines(lines: List[Dict]) -> List[Line]:
    """
    Return a list containing parsed lines from OpenApi response
    """
    return [_parse_line(line["values"]) for line in lines]


def _parse_timeline(timeline: List[Dict]) -> Timeline:
    _attrs = {val["key"]: val["value"] for val in timeline}
    return Timeline(
        arrival_time=datetime.strptime(_attrs["czas"], "%H:%M:%S").time(),
        direction=_attrs["kierunek"],
        brigade=_attrs["brygada"],
    )


def parse_timetable(timetable: List[Dict], line: str) -> Timetable:
    """
    Return a timetable for particular line containing arrival timelines.
    """
    timelines = [_parse_timeline(timeline["values"]) for timeline in timetable]
    return Timetable(timelines, line)


def get_next_arrival_timeline(timetable: Timetable) -> Timeline | None:
    """
    Returns next arrival timeline (arrival time, direction and brigade)
    from now for a given line stop timetable.
    """
    now = _current_time()
    max_time_delta = datetime.combine(now, time().max) - now
    nat = None
    for timeline in timetable.timelines:
        arrival_timedate = datetime.combine(now, timeline.arrival_time)
        time_delta = arrival_timedate - now
        if time_delta < max_time_delta and arrival_timedate >= now:
            max_time_delta = time_delta
            nat = timeline
    return nat


def _current_time():
    return datetime.now()


def _parse_vehicle_location(location: Dict) -> Coordinates:
    return Coordinates(lat=location["Lat"], lon=location["Lon"])


def parse_vehicle_locations(locations: List[Dict]) -> List[Coordinates]:
    """
    Return locations of Coordinates for given from OpenApi response.
    """
    return [_parse_vehicle_location(location) for location in locations]
