from domain.model import Coordinates
from utils.utils import (
    calculate_haversine_distance,
    parse_stops,
    closest_stop,
    parse_lines,
)
from domain.model import BusStop
from utils.api_requests import get_stops_coordinates, get_stop_lines
from wawa_transport_api.utils.api_requests import get_stop_timetable


my_position = Coordinates(52.243552, 21.077855)


def test_calculate_distance():
    stops = get_stops_coordinates()
    stop = closest_stop(parse_stops(stops), my_position)
    assert stop.name == "Grenadierów"
    assert stop.number == "04"


def test_calculate_haversine_distance():
    stops = get_stops_coordinates()
    stop = closest_stop(
        parse_stops(stops), my_position, distance_func=calculate_haversine_distance
    )
    assert stop.name == "Grenadierów"
    assert stop.number == "04"


def test_parse_lines():
    stops = get_stops_coordinates()
    stop = closest_stop(
        parse_stops(stops), my_position, distance_func=calculate_haversine_distance
    )

    lines = parse_lines(get_stop_lines(stop.id, stop.number))
    timetables = {
        line.number: get_stop_timetable(stop.id, stop.number, line.number)
        for line in lines
    }
