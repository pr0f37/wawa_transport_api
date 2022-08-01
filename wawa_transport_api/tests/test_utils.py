from datetime import datetime, time
from unittest.mock import Mock

from wawa_transport_api.domain.model import Coordinates, Line, Timeline, Timetable
from wawa_transport_api.tests.fixtures import (
    _fake_get_stop_lines,
    _fake_get_stop_timetable,
    _fake_get_stops_coordinates,
    _fake_get_vehicle_location,
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


def _get_closest_stop(_fake_get_stops_coordinates, distance_func=None):
    my_position = Coordinates(52.243552, 21.077855)
    stops = _fake_get_stops_coordinates
    if distance_func:
        return closest_stop(
            parse_stops(stops), my_position, distance_func=distance_func
        )
    return closest_stop(parse_stops(stops), my_position)


def test_calculate_distance(_fake_get_stops_coordinates):
    stop = _get_closest_stop(_fake_get_stops_coordinates)
    assert stop.name == "Grenadierów"
    assert stop.number == "04"
    assert stop.id == "2134"
    assert stop.direction == "Wiatraczna"


def test_calculate_haversine_distance(_fake_get_stops_coordinates):
    stop = _get_closest_stop(
        _fake_get_stops_coordinates, distance_func=calculate_haversine_distance
    )
    assert stop.name == "Grenadierów"
    assert stop.number == "04"


def test_parse_lines(_fake_get_stop_lines):
    lines = parse_lines(_fake_get_stop_lines)
    assert isinstance(lines, list)
    for line in lines:
        assert isinstance(line, Line)
        assert isinstance(line.number, str)


def _parse_timetables(_fake_get_stop_lines, _fake_get_stop_timetable):
    lines = parse_lines(_fake_get_stop_lines)
    return [
        parse_timetable(_fake_get_stop_timetable(line.number), line.number)
        for line in lines
    ]


def test_parse_timetable(_fake_get_stop_lines, _fake_get_stop_timetable):
    timetables = _parse_timetables(_fake_get_stop_lines, _fake_get_stop_timetable)
    for timetable in timetables:
        isinstance(timetable, Timetable)
        isinstance(timetable.line, str)
        for timeline in timetable.timelines:
            isinstance(timeline, Timeline)
            isinstance(timeline.arrival_time, time)
            isinstance(timeline.brigade, str)
            isinstance(timeline.direction, str)


def test_find_next_arrival(_fake_get_stop_lines, _fake_get_stop_timetable, mocker):
    mocker.patch(
        "wawa_transport_api.utils.utils._current_time",
        Mock(return_value=datetime.combine(datetime.now(), time().min)),
    )
    timetables = _parse_timetables(_fake_get_stop_lines, _fake_get_stop_timetable)
    next_arrivals = {
        timetable.line: get_next_arrival_timeline(timetable=timetable)
        for timetable in timetables
    }
    for arrival in next_arrivals.values():
        if arrival.arrival_time:
            assert arrival.arrival_time > time().min


def test_get_vehicles_locations(
    _fake_get_stop_lines, _fake_get_stop_timetable, _fake_get_vehicle_location, mocker
):
    mocker.patch(
        "wawa_transport_api.utils.utils._current_time",
        Mock(return_value=datetime.combine(datetime.now(), time().min)),
    )
    timetables = _parse_timetables(_fake_get_stop_lines, _fake_get_stop_timetable)
    next_arrivals = {
        timetable.line: get_next_arrival_timeline(timetable=timetable)
        for timetable in timetables
    }
    locations = [
        parse_vehicle_locations(_fake_get_vehicle_location(line, timeline.brigade))
        for line, timeline in next_arrivals.items()
    ]
    for location in locations:
        assert isinstance(location, list)
        for coords in location:
            assert isinstance(coords, Coordinates)
