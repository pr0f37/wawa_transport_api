from typing import Dict, List
import requests
import configparser

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
