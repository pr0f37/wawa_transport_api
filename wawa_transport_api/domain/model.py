"""Domain models"""
from dataclasses import dataclass
from datetime import time
from typing import List


@dataclass
class Coordinates:
    """
    Class representing geographical coordinates

    Properties:
        lat: float
        lon: float
    """

    lat: float
    lon: float


@dataclass
class BusStop:
    """
    Class representing the bus or tram stop

    Properties:
        id: str
        number: str
        coords: Coordinates
        name: str
        direction: str
    """

    id: str
    number: str
    coords: Coordinates
    name: str
    direction: str


@dataclass
class Line:
    """
    Class representing line

    Properties:
        number: str
    """

    number: str


@dataclass
class Timeline:
    """
    Class representing single arrival timeline in timetable

    Properties:
        arrival_time: time
        direction: str
        brigade: str
    """

    arrival_time: time
    direction: str
    brigade: str


@dataclass
class Timetable:
    """
    Class representing timeline for single line on a bus/tram stop

    Properties:
        timelines: List[Timeline]
        line: Line
    """

    timelines: List[Timeline]
    line: Line
