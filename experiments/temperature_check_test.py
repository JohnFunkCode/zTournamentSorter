#Written by ChatGPT

import unittest
import temperature_check as tc

class TestTemperatureCheck(unittest.TestCase):
    def test_hot_temperature(self):
        result = tc.temperature_check(85)
        self.assertEqual(result, "it's hot")

    def test_cold_temperature(self):
        result = tc.temperature_check(35)
        self.assertEqual(result, "it's cold")

    def test_mild_temperature(self):
        result = tc.temperature_check(65)
        self.assertEqual(result, "it's mild")


if __name__ == '__main__':
    unittest.main()
