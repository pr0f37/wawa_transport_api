import configparser
from typing import Dict, List

import requests

config = configparser.ConfigParser()
config.read("config.ini")
API_KEY = config["OPENAPI"]["api_key"]


def get_stops_coordinates() -> List[Dict]:
    """
    Fetch bus and tram stops coordinates from Warsaw UM Open Api.

    Returns:
        List[Dict]: List of objects representing bus and tram stops
    """
    payload = {
        "id": "ab75c33d-3a26-4342-b36a-6e5fef0a3ac3",
        "apikey": API_KEY,
    }
    response = requests.get(
        "https://api.um.warszawa.pl/api/action/dbstore_get", params=payload
    )
    stops = response.json()["result"]
    return stops


def get_stop_lines(stop_id: str, stop_number: str) -> List[Dict]:
    """
    Fetch lines arriving at stop.
    Returns:
        List[Dict]: timetable for given line
    """
    payload = {
        "id": "88cd555f-6f31-43ca-9de4-66c479ad5942",
        "apikey": API_KEY,
        "busstopId": stop_id,
        "busstopNr": stop_number,
    }

    response = requests.get(
        "https://api.um.warszawa.pl/api/action/dbtimetable_get", params=payload
    )
    lines = response.json()["result"]
    return lines


def get_stop_timetable(stop_id: str, stop_number: str, line_number: str) -> List[Dict]:
    """
    Fetch timetable for given bus stop.
    Returns:
        List[Dict]: timetable for given line
    """
    payload = {
        "id": "e923fa0e-d96c-43f9-ae6e-60518c9f3238",
        "apikey": API_KEY,
        "busstopId": stop_id,
        "busstopNr": stop_number,
        "line": line_number,
    }

    response = requests.get(
        "https://api.um.warszawa.pl/api/action/dbtimetable_get", params=payload
    )
    timetable = response.json()["result"]
    return timetable
