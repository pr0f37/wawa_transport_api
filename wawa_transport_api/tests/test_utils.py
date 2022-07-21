from domain.model import Coordinates
from utils.utils import calculate_haversine_distance, parse_bus_stops, closest_stop
from domain.model import BusStop
from utils.api_requests import get_stops_coordinates

my_position = Coordinates(52.243552, 21.077855)


def test_calculate_distance():
    stops = get_stops_coordinates()
    stop = closest_stop(parse_bus_stops(stops), my_position)
    assert stop.name == "Grenadierów"
    assert stop.number == "04"


def test_calculate_haversine_distance():
    stops = get_stops_coordinates()
    stop = closest_stop(
        parse_bus_stops(stops), my_position, distance_func=calculate_haversine_distance
    )
    assert stop.name == "Grenadierów"
    assert stop.number == "04"
    pass
