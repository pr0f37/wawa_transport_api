from typing import Tuple
from wawa_transport_api.domain.model import Coordinates, ScheduleItem, Timeline
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

LOCATION = Coordinates(52.243552, 21.077855)


def get_schedule_for_location(my_location: Coordinates = LOCATION):
    def _common_entries(*dcts) -> Tuple[str, Timeline, Coordinates]:
        if not dcts:
            return
        return [
            (i,) + tuple(d[i] for d in dcts)
            for i in set(dcts[0]).intersection(*dcts[1:])
        ]

    stops = get_stops_coordinates()
    stop = closest_stop(parse_stops(stops), my_location)
    lines = parse_lines(get_stop_lines(stop.id, stop.number))
    timetables = [
        parse_timetable(
            get_stop_timetable(stop.id, stop.number, line.number), line.number
        )
        for line in lines
    ]
    next_arrivals = {
        timetable.line: get_next_arrival_timeline(timetable=timetable)
        for timetable in timetables
    }
    locations = {
        line: parse_vehicle_locations(
            get_vehicle_location(line=line, brigade=timeline.brigade)
        )
        for line, timeline in next_arrivals.items()
    }
    locations = {
        line: location.pop() if location else None
        for line, location in locations.items()
    }
    schedule = [
        ScheduleItem(
            line=line,
            direction=timeline.direction,
            arrival_time=timeline.arrival_time,
            position=coordinates,
        )
        for line, timeline, coordinates in _common_entries(next_arrivals, locations)
    ]

    return stop, schedule


if __name__ == "__main__":
    stop, schedule = get_schedule_for_location(LOCATION)
    print(f"Closest stop name {stop.name} {stop.number}")
    print(
        "This stop is located",
        f"{calculate_haversine_distance(stop, LOCATION):.2f}",
        "km from you",
    )
    print("Schedule:")
    for item in sorted(schedule, key=lambda x: x.arrival_time):
        print(f"Line: {item.line} -> {item.direction}")
        print(f"Arrives at: {item.arrival_time}")
        print(
            "Distance from the stop:",
            f"{calculate_haversine_distance(stop, item.position):.2f} km",
        )
