import unittest
from jsonmodeler.json_parser import JSONParser


class TestJSONParser(unittest.TestCase):

    def test_parse_valid_json(self):
        json_data = '{"name": "John", "age": 30, "is_student": false}'
        expected = {
            "name": "John",
            "age": 30,
            "is_student": False
        }
        result = JSONParser.parse(json_data)
        self.assertEqual(result, expected)

    def test_parse_invalid_json(self):
        json_data = '{"name": "John", "age": 30, "is_student": false'
        with self.assertRaises(ValueError) as context:
            JSONParser.parse(json_data)
        self.assertTrue('Invalid JSON data' in str(context.exception))

    def test_from_file_valid(self):
        file_path = './test_data/valid.json'
        expected = {
            "name": "John",
            "age": 30,
            "is_student": False
        }
        result = JSONParser.from_file(file_path)
        self.assertEqual(result, expected)

    def test_from_file_invalid(self):
        file_path = '/test_data/invalid.json'
        with self.assertRaises(ValueError) as context:
            JSONParser.from_file(file_path)
        self.assertTrue('Error reading file' in str(context.exception))


if __name__ == "__main__":
    unittest.main()
