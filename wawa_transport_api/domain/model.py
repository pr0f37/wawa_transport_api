"""Domain models"""
from dataclasses import dataclass
from datetime import time


@dataclass
class Coordinates:
    """Class representing geographical coordinates"""

    lat: float
    lon: float


@dataclass
class BusStop:
    """Class representing the bus or tram stop"""

    id: str
    number: str
    coords: Coordinates
    name: str
    direction: str


@dataclass
class Line:
    """Class representing line"""

    number: str


@dataclass
class Timetable:
    """Class representing stop timetable"""

    arrival_time: time
    direction: str
    brigade: str
