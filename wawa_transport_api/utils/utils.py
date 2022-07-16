"""Module containing methods to be used across the application"""
import configparser
from typing import Dict, List
import requests

from wawa_transport_api.domain.model import BusStop


def _parse_stops_coordinates(stops: List[Dict]) -> List[BusStop]:
    return [_parse_bus_stop(stop["values"]) for stop in stops]


def _parse_bus_stop(stop: Dict) -> BusStop:
    _attrs = {val["key"]: val["value"] for val in stop}
    return BusStop(
        id=_attrs["zespol"],
        number=_attrs["slupek"],
        lat=float(_attrs["szer_geo"]),
        lon=float(_attrs["dlug_geo"]),
    )


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
    stops = _parse_stops_coordinates(r.json()["result"])
    pass
