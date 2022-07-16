"""Domain models"""
from dataclasses import dataclass


@dataclass
class BusStop:
    """Class representing the buss or tram stop"""

    id: str
    number: str
    lat: float
    lon: float
