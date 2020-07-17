import datetime
from django.test import SimpleTestCase
from unittest import TestCase

from schedule.models import Weather, Parameter, ReportType

class ReportingTestCase(SimpleTestCase):
    """All of the reporting methods using djangos test case object
    
    From the command line use -> python manage.py test schedule.tests.ReportingTestCase.testDaysOfYear"""
    def testGanttWeather(self):
        weather = Weather(2)
        weather.schedule.StatusTypeId = 1
        activities = weather.CalcScheduleDuration()[0]
        self.assertEqual(activities[-1].EndDate, datetime.date(2019, 3, 14))

    def testGanttWeatherStatusdate(self):
        weather = Weather(2)
        weather.schedule.StatusDate = datetime.date(2017, 4, 1)
        weather.schedule.StatusTypeId = 2
        result = weather.CalcScheduleDuration()
        self.assertEqual(result[0][-1].EndDate, datetime.date(2018, 12, 31))

    def testDaysOfYear(self):
        weather = Weather(2)
        weather.schedule.StatusTypeId = 1
        durationList, endDateList = weather.CalcDaysOfYear()
        averageDuration = sum(durationList) / 365
        assert len(durationList) == 365
        assert int(averageDuration) == 570

    def testGanttReverse(self):
        weather = Weather(2)
        weather.schedule.StatusTypeId = 1

        # get the end date with no weather aware extensions
        result = weather.CalcScheduleDuration(calcType=ReportType.NORMAL)
        originalEndDate = result[0][-1].EndDate

        # now go forwards and then backwards
        result = weather.CalcScheduleDuration(calcType=ReportType.WEATHER_AWARE)

        for idx, activity in enumerate(weather.activityList):
            weather.activityList[idx].Duration = result[0][idx].NewDuration

        result = weather.CalcScheduleDuration(calcType=ReportType.REVERSE)

        for idx, activity in enumerate(weather.activityList):
            weather.activityList[idx].Duration = result[0][idx].NewDuration

        result = weather.CalcScheduleDuration(calcType=ReportType.NORMAL)
        reversedEndDate = result[0][-1].EndDate

        self.assertEqual(originalEndDate, reversedEndDate)

    def testStochastic(self):
        weather = Weather(2)
        weather.schedule.StatusTypeId = 1
        durationList = weather.CalcStochastic(100, reportType=ReportType.WEATHER_AWARE)
        averageDays = sum(days for probability, days in durationList) / 100
        assert 550.0 <= averageDays <= 570.0

    def testStochasticStatusDate(self):
        weather = Weather(2)
        weather.schedule.StatusDate = datetime.date(2017, 4, 1)
        weather.schedule.StatusTypeId = 2
        durationList = weather.CalcStochastic(100, reportType=ReportType.WEATHER_AWARE)
        averageDays = sum(days for probability, days in durationList) / 100
        assert 510.0 <= averageDays <= 530.0

    def testReverseStochastic(self):
        weather = Weather(2)
        weather.schedule.StatusTypeId = 1
        durationList = weather.CalcStochastic(100, reportType=ReportType.REVERSE)
        averageDays = sum(days for probability, days in durationList) / 100
        assert 470.0 <= averageDays <= 490.0

class WeatherMethodsTestCase(TestCase):
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
