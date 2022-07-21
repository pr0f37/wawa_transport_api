"""Domain models"""
from dataclasses import dataclass


@dataclass
class Coordinates:
    """Class representing geographical coordinates"""

    lat: float
    lon: float


@dataclass
class BusStop:
    """Class representing the buss or tram stop"""

    id: str
    number: str
    coords: Coordinates
    name: str
    direction: str
