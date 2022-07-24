from wawa_transport_api.domain.model import BusStop, Coordinates
from wawa_transport_api.utils.api_requests import (
    get_stop_lines,
    get_stop_timetable,
    get_vehicle_location,
)

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


def test_get_vehicle_location():
    location = get_vehicle_location("9", "2")
    isinstance(location, list)
