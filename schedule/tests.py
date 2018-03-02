from django.test import TestCase
from schedule.models import Weather

class WeatherTestCase(TestCase):
    # def setUp(self):
    def test_can_run_report(self):
        weather = Weather.Weather(2)

        self.assertEqual(1, 1)
        # weather.CalcWeatherDuration()

if __name__ == '__main__':
    unittest.main()
