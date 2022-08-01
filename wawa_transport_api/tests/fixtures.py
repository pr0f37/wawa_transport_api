import pytest


@pytest.fixture
def _fake_get_stop_lines():
    return [
        {"values": [{"value": "9", "key": "linia"}]},
        {"values": [{"value": "24", "key": "linia"}]},
    ]


@pytest.fixture
def _fake_get_stops_coordinates():
    return [
        {
            "values": [
                {"value": "2134", "key": "zespol"},
                {"value": "04", "key": "slupek"},
                {"value": "Grenadierów", "key": "nazwa_zespolu"},
                {"value": "0151", "key": "id_ulicy"},
                {"value": "52.243536", "key": "szer_geo"},
                {"value": "21.078492", "key": "dlug_geo"},
                {"value": "Wiatraczna", "key": "kierunek"},
                {"value": "2022-03-26 00:00:00.0", "key": "obowiazuje_od"},
            ]
        },
        {
            "values": [
                {"value": "1001", "key": "zespol"},
                {"value": "01", "key": "slupek"},
                {"value": "Kijowska", "key": "nazwa_zespolu"},
                {"value": "2201", "key": "id_ulicy"},
                {"value": "52.248455", "key": "szer_geo"},
                {"value": "21.044827", "key": "dlug_geo"},
                {"value": "al.Zieleniecka", "key": "kierunek"},
                {"value": "2022-03-26 00:00:00.0", "key": "obowiazuje_od"},
            ]
        },
    ]


@pytest.fixture
def _fake_get_stop_timetable():
    def _select_line(line_number):
        if line_number == "9":
            return [
                {
                    "values": [
                        {"value": "null", "key": "symbol_2"},
                        {"value": "null", "key": "symbol_1"},
                        {"value": "2", "key": "brygada"},
                        {"value": "Goc\\u0142awek", "key": "kierunek"},
                        {"value": "TD-2GCWW", "key": "trasa"},
                        {"value": "04:19:00", "key": "czas"},
                    ]
                },
                {
                    "values": [
                        {"value": "null", "key": "symbol_2"},
                        {"value": "null", "key": "symbol_1"},
                        {"value": "3", "key": "brygada"},
                        {"value": "Goc\\u0142awek", "key": "kierunek"},
                        {"value": "TD-3GCW", "key": "trasa"},
                        {"value": "04:39:00", "key": "czas"},
                    ]
                },
            ]
        if line_number == "24":
            return [
                {
                    "values": [
                        {"value": "null", "key": "symbol_2"},
                        {"value": "null", "key": "symbol_1"},
                        {"value": "6", "key": "brygada"},
                        {"value": "Goc\\u0142awek", "key": "kierunek"},
                        {"value": "TD-1GCW", "key": "trasa"},
                        {"value": "05:07:00", "key": "czas"},
                    ]
                },
                {
                    "values": [
                        {"value": "null", "key": "symbol_2"},
                        {"value": "null", "key": "symbol_1"},
                        {"value": "9", "key": "brygada"},
                        {"value": "Goc\\u0142awek", "key": "kierunek"},
                        {"value": "TP-GCW", "key": "trasa"},
                        {"value": "05:47:00", "key": "czas"},
                    ]
                },
            ]
        return None

    return _select_line


@pytest.fixture
def _fake_get_vehicle_location():
    def _select_line(line_number, brigade_number):
        if line_number == "9" and brigade_number == "2":
            return [
                {
                    "Lines": "9",
                    "Lon": 21.016388,
                    "VehicleNumber": "3183",
                    "Time": "2022-08-01 22:37:50",
                    "Lat": 52.23082,
                    "Brigade": "2",
                }
            ]
        if line_number == "24" and brigade_number == "6":
            return [
                {
                    "Lines": "24",
                    "Lon": 20.958994,
                    "VehicleNumber": "1281+1282",
                    "Time": "2022-08-01 22:40:34",
                    "Lat": 52.24744,
                    "Brigade": "6",
                }
            ]
        return None

    return _select_line
