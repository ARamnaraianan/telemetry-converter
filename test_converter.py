import json
import unittest
from converter import convertFromFormat1, convertFromFormat2


def load_json(path):
    with open(path) as f:
        return json.load(f)


class TestConvertFromFormat1(unittest.TestCase):
    def test_conversion_matches_expected_result(self):
        data1 = load_json("data-1.json")
        expected = load_json("data-result.json")
        result = convertFromFormat1(data1)
        self.assertEqual(result, expected)

    def test_location_is_split_into_parts(self):
        data = {
            "deviceID": "test-1",
            "deviceType": "sensor",
            "timestamp": 1000000,
            "location": "Germany/Berlin/Mitte/PlantB/Zone3",
            "operationStatus": "active",
            "temp": 18.0,
        }
        result = convertFromFormat1(data)
        self.assertEqual(result["location"]["country"], "Germany")
        self.assertEqual(result["location"]["city"], "Berlin")
        self.assertEqual(result["location"]["area"], "Mitte")
        self.assertEqual(result["location"]["factory"], "PlantB")
        self.assertEqual(result["location"]["section"], "Zone3")

    def test_other_fields_are_preserved(self):
        data = {
            "deviceID": "test-2",
            "deviceType": "actuator",
            "timestamp": 9999999,
            "location": "France/Paris/Montmartre/PlantC/SectionX",
            "operationStatus": "inactive",
            "temp": 30.0,
        }
        result = convertFromFormat1(data)
        self.assertEqual(result["deviceID"], "test-2")
        self.assertEqual(result["deviceType"], "actuator")
        self.assertEqual(result["timestamp"], 9999999)
        self.assertEqual(result["operationStatus"], "inactive")
        self.assertEqual(result["temp"], 30.0)

    def test_invalid_location_raises_value_error(self):
        data = {
            "deviceID": "test-x",
            "deviceType": "sensor",
            "timestamp": 1000,
            "location": "USA/NewYork",
            "operationStatus": "active",
            "temp": 20.0,
        }
        with self.assertRaises(ValueError):
            convertFromFormat1(data)


class TestConvertFromFormat2(unittest.TestCase):
    def test_conversion_matches_expected_result(self):
        data2 = load_json("data-2.json")
        expected = load_json("data-result.json")
        result = convertFromFormat2(data2)
        self.assertEqual(result, expected)

    def test_iso_timestamp_converted_to_ms(self):
        data = {
            "deviceID": "test-3",
            "deviceType": "sensor",
            "timestamp": "2020-11-04T00:00:00.000Z",
            "location": {
                "country": "USA",
                "city": "NewYork",
                "area": "Manhattan",
                "factory": "FactoryA",
                "section": "Section1",
            },
            "operationStatus": "active",
            "temp": 23.5,
        }
        result = convertFromFormat2(data)
        self.assertEqual(result["timestamp"], 1604448000000)

    def test_location_object_is_preserved(self):
        data = {
            "deviceID": "test-4",
            "deviceType": "sensor",
            "timestamp": "2021-06-15T12:30:00.000Z",
            "location": {
                "country": "Canada",
                "city": "Toronto",
                "area": "Downtown",
                "factory": "PlantD",
                "section": "SectionY",
            },
            "operationStatus": "active",
            "temp": 20.0,
        }
        result = convertFromFormat2(data)
        self.assertEqual(result["location"]["country"], "Canada")
        self.assertEqual(result["location"]["city"], "Toronto")
        self.assertEqual(result["location"]["area"], "Downtown")
        self.assertEqual(result["location"]["factory"], "PlantD")
        self.assertEqual(result["location"]["section"], "SectionY")

    def test_other_fields_are_preserved(self):
        data = {
            "deviceID": "test-5",
            "deviceType": "actuator",
            "timestamp": "2020-01-01T00:00:00.000Z",
            "location": {
                "country": "UK",
                "city": "London",
                "area": "City",
                "factory": "PlantE",
                "section": "SectionZ",
            },
            "operationStatus": "maintenance",
            "temp": 15.0,
        }
        result = convertFromFormat2(data)
        self.assertEqual(result["deviceID"], "test-5")
        self.assertEqual(result["deviceType"], "actuator")
        self.assertEqual(result["operationStatus"], "maintenance")
        self.assertEqual(result["temp"], 15.0)


if __name__ == "__main__":
    unittest.main()
