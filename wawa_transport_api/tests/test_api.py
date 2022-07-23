from domain.model import Coordinates

from utils.api_requests import get_stops_coordinates, get_stop_timetable
from wawa_transport_api.domain.model import BusStop
from wawa_transport_api.utils.api_requests import get_stop_lines

stop = BusStop(
    id="2134",
    number="04",
    coords=Coordinates(lat=52.243536, lon=21.078492),
    name="Grenadierów",
    direction="Wiatraczna",
)


def test_get_stop_lines():
    lines = get_stop_lines(stop.id, stop.number)
    isinstance(lines, list)


def test_get_stop_timetable():
    timetable = get_stop_timetable(stop.id, stop.number, "9")
    isinstance(timetable, list)
