from django.test import TestCase
from schedule.models import Weather, Parameter
import datetime

class WeatherTestCase(TestCase):
    # def setUp(self):
    def test_can_run_report(self):
        weather = Weather(2)
        activities = weather.CalcScheduleDuration()
        self.assertEqual(activities[-1].EndDate, datetime.date(2019, 3, 14))

class TestWeatherMethods(TestCase):
    @classmethod
    def setUp(cls):
        # earthworks, lat = -0.9, long = 49.0
        parameter = Parameter
        parameter.K = 0.92136791170900
        parameter.A = 0.05115897489560
        parameter.P = 0.44740549870600
        cls._parameter = parameter
        cls._standardWorkingDays = [1, 1, 1, 1, 1, 0, 0]

    def test0(self):
        self.assertEqual(Weather.GetAdjustedDate(datetime.date(2018, 1, 8), self._standardWorkingDays, 0), datetime.date(2018, 1, 8))

    def testPlus1(self):
        self.assertEqual(Weather.GetAdjustedDate(datetime.date(2018, 1, 8), self._standardWorkingDays, 1), datetime.date(2018, 1, 9))

    def testPlus1Weekend(self):
        self.assertEqual(Weather.GetAdjustedDate(datetime.date(2018, 1, 5), self._standardWorkingDays, 1), datetime.date(2018, 1, 8))

    def testPlus1WeekendAllowed(self):
        self.assertEqual(Weather.GetAdjustedDate(datetime.date(2018, 1, 5), [1, 1, 1, 1, 1, 1, 1], 1), datetime.date(2018, 1, 6))

    def testPlus10(self):
        self.assertEqual(Weather.GetAdjustedDate(datetime.date(2018, 1, 1), self._standardWorkingDays, 10), datetime.date(2018, 1, 15))

    def testMinus1(self):
        self.assertEqual(Weather.GetAdjustedDate(datetime.date(2018, 1, 9), self._standardWorkingDays, -1), datetime.date(2018, 1, 8))

    def testMinus1Weekend(self):
        self.assertEqual(Weather.GetAdjustedDate(datetime.date(2018, 1, 8), self._standardWorkingDays, -1), datetime.date(2018, 1, 5))

    def testMinus1WeekendAllowed(self):
        self.assertEqual(Weather.GetAdjustedDate(datetime.date(2018, 1, 8), [1, 1, 1, 1, 1, 1, 1], -1), datetime.date(2018, 1, 7))

    def testPlus10WeatherEffected(self):
        self.assertEqual(Weather.GetAdjustedDate(datetime.date(2018, 1, 1), self._standardWorkingDays, 10, self._parameter), datetime.date(2018, 1, 17))

    def testMinus10WeatherEffected(self):
        self.assertEqual(Weather.GetAdjustedDate(datetime.date(2018, 1, 17), self._standardWorkingDays, -10, self._parameter), datetime.date(2018, 1, 1))


if __name__ == '__main__':
    unittest.main()
