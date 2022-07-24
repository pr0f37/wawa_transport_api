from datetime import datetime, time

from wawa_transport_api.domain.model import Coordinates, Line, Timeline, Timetable
from wawa_transport_api.utils.api_requests import (
    get_stop_lines,
    get_stop_timetable,
    get_stops_coordinates,
    get_vehicle_location,
)
from wawa_transport_api.utils.utils import (
    calculate_haversine_distance,
    closest_stop,
    get_next_arrival_timeline,
    parse_lines,
    parse_stops,
    parse_timetable,
    parse_vehicle_locations,
)


def _get_closest_stop(distance_func=None):
    my_position = Coordinates(52.243552, 21.077855)
    stops = get_stops_coordinates()
    if distance_func:
        return closest_stop(
            parse_stops(stops), my_position, distance_func=distance_func
        )
    return closest_stop(parse_stops(stops), my_position)


def test_calculate_distance():
    stop = _get_closest_stop()
    assert stop.name == "Grenadierów"
    assert stop.number == "04"


def test_calculate_haversine_distance():
    stop = _get_closest_stop(distance_func=calculate_haversine_distance)
    assert stop.name == "Grenadierów"
    assert stop.number == "04"


def _parse_lines():
    stop = _get_closest_stop()
    return parse_lines(get_stop_lines(stop.id, stop.number))


def test_parse_lines():
    lines = _parse_lines()
    assert isinstance(lines, list)
    for line in lines:
        assert isinstance(line, Line)
        assert isinstance(line.number, str)


def _parse_timetables():
    stop = _get_closest_stop()
    lines = _parse_lines()
    return [
        parse_timetable(
            get_stop_timetable(stop.id, stop.number, line.number), line.number
        )
        for line in lines
    ]


def test_parse_timetable():
    timetables = _parse_timetables()
    for timetable in timetables:
        isinstance(timetable, Timetable)
        isinstance(timetable.line, str)
        for timeline in timetable.timelines:
            isinstance(timeline, Timeline)
            isinstance(timeline.arrival_time, time)
            isinstance(timeline.brigade, str)
            isinstance(timeline.direction, str)


def test_find_next_arrival():
    timetables = _parse_timetables()
    next_arrivals = {
        timetable.line: get_next_arrival_timeline(timetable=timetable)
        for timetable in timetables
    }
    for arrival in next_arrivals.values():
        if arrival.arrival_time:
            assert arrival.arrival_time > datetime.now().time()


def test_get_vehicles_locations():
    timetables = _parse_timetables()
    next_arrivals = {
        timetable.line: get_next_arrival_timeline(timetable=timetable)
        for timetable in timetables
    }
    locations = [
        parse_vehicle_locations(
            get_vehicle_location(line=line, brigade=timeline.brigade)
        )
        for line, timeline in next_arrivals.items()
    ]
    pass
