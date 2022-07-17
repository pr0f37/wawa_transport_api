"""Module containing methods to be used across the application"""
import configparser
from math import pi, sin, cos, atan2, sqrt
from typing import Dict, Generator, List
import requests

from wawa_transport_api.domain.model import BusStop, Coordinates


def parse_stops_coordinates(stops: List[Dict]) -> Generator[BusStop, None, None]:
    """
    Return a generator function containing a list of bus stops parsed
    from OpenApi response
    """
    return (_parse_bus_stop(stop["values"]) for stop in stops)


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


def calculate_distance(stop: BusStop, current_position: Coordinates) -> float:
    """
    Calculate distance between current position and a bus stop
    """
    return abs(stop.coords.lat - current_position.lat) + abs(
        stop.coords.lon - current_position.lon
    )


def calculate_haversine_distance(stop: BusStop, current_position: Coordinates) -> float:
    """
    Calculate distance between current position and a bus stop using haversine formulae
    Not sure if the calculation is entirely correct as the resulting distance seems to be
    way too large.
    """

    def _deg2rad(deg):
        return deg * (pi / 180)

    R = 6387
    dist_lat = _deg2rad(stop.coords.lat - current_position.lat)
    dist_lon = _deg2rad(stop.coords.lon - current_position.lon)
    a = (sin(dist_lat / 2) ** 2) + cos(_deg2rad(stop.coords.lat)) * cos(
        _deg2rad(current_position.lat)
    ) * (sin(dist_lon / 2) ** 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = R * c
    return d


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    api_key = config["OPENAPI"]["api_key"]
    payload = {
        "id": "ab75c33d-3a26-4342-b36a-6e5fef0a3ac3",
        "page": 1,
        "size": 5,
        "apikey": api_key,
    }
    r = requests.get(
        "https://api.um.warszawa.pl/api/action/dbstore_get", params=payload
    )
    stops = r.json()["result"]

    my_position = Coordinates(52.243552, 21.077855)
    distances = {
        calculate_distance(stop=stop, current_position=my_position): stop
        for stop in parse_stops_coordinates(stops)
    }
    min_dist = float("inf")
    closest_stops = []
    for stop in parse_stops_coordinates(stops):
        dist = calculate_distance(stop=stop, current_position=my_position)
        if dist < min_dist:
            closest_stops = [stop]
            min_dist = dist
        elif dist == min_dist:
            closest_stops.append(stop)
    min_dist = float("inf")
    closest_h_stops = []
    for stop in parse_stops_coordinates(stops):
        h_dist = calculate_haversine_distance(stop=stop, current_position=my_position)
        if h_dist < min_dist:
            closest_h_stops = [stop]
            min_dist = h_dist
        elif h_dist == min_dist:
            closest_h_stops.append(stop)
    pass
