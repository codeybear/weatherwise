import datetime
from django.test import SimpleTestCase

from schedule.models import Weather, Parameter, ReportType

class WeatherTestCase(SimpleTestCase):
    # def setUp(self):
    def test_can_run_report(self):
        weather = Weather(2)
        activities = weather.CalcScheduleDuration()[0]
        self.assertEqual(activities[-1].EndDate, datetime.date(2019, 3, 14))

    def test_can_run_report_reverse(self):
        weather = Weather(2)
        weather.schedule.StatusTypeId = 1

        result = weather.CalcScheduleDuration(calcType=ReportType.NORMAL)
        originalEndDate = result[0][-1].EndDate

        result = weather.CalcScheduleDuration(calcType=ReportType.WEATHER_AWARE)

        for idx, activity in enumerate(weather.activityList):
            weather.activityList[idx].Duration = result[0][idx].NewDuration

        result = weather.CalcScheduleDuration(calcType=ReportType.REVERSE)
        reversedEndDate = result[0][-1].EndDate

        assert originalEndDate == reversedEndDate

class TestWeatherMethods(SimpleTestCase):
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
